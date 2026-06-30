package com.saarthi.agent;

import net.bytebuddy.agent.builder.AgentBuilder;
import net.bytebuddy.asm.Advice;
import net.bytebuddy.description.type.TypeDescription;
import net.bytebuddy.dynamic.DynamicType;
import net.bytebuddy.matcher.ElementMatchers;
import net.bytebuddy.utility.JavaModule;

import java.lang.instrument.Instrumentation;
import java.lang.reflect.Method;
import java.util.Map;
import java.util.HashMap;
import java.util.Collections;
import java.util.WeakHashMap;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

public class SaarthiAgent {

    public static final Map<Object, String> preparedStatementSqlMap = Collections.synchronizedMap(new WeakHashMap<>());
    private static final AtomicInteger transformedClassesCount = new AtomicInteger(0);
    private static final AtomicBoolean servletDetected = new AtomicBoolean(false);
    private static final AtomicBoolean springDetected = new AtomicBoolean(false);
    private static final AtomicBoolean jdbcDetected = new AtomicBoolean(false);

    public static void premain(String agentArgs, Instrumentation inst) {
        System.out.println("[SaarthiAgent] Java agent premain() starting...");

        String endpoint = "http://localhost:8081/events";
        if (agentArgs != null && !agentArgs.trim().isEmpty()) {
            String[] args = agentArgs.split(",");
            for (String arg : args) {
                if (arg.startsWith("endpoint=")) {
                    endpoint = arg.substring("endpoint=".length());
                }
            }
        }
        EventPublisher.setAdapterUrl(endpoint);

        AgentBuilder.Listener listener = new AgentBuilder.Listener() {
            @Override
            public void onDiscovery(String typeName, ClassLoader classLoader, JavaModule module, boolean loaded) {}

            @Override
            public void onTransformation(TypeDescription typeDescription, ClassLoader classLoader, JavaModule module, boolean loaded, DynamicType dynamicType) {
                transformedClassesCount.incrementAndGet();
                String name = typeDescription.getName();
                if (name.contains("servlet.http.HttpServlet")) servletDetected.set(true);
                if (name.contains("springframework.web.servlet.DispatcherServlet")) springDetected.set(true);
                if (name.contains("sql.PreparedStatement") || name.contains("sql.Statement") || name.contains("sql.Connection")) jdbcDetected.set(true);
            }

            @Override
            public void onIgnored(TypeDescription typeDescription, ClassLoader classLoader, JavaModule module, boolean loaded) {}

            @Override
            public void onError(String typeName, ClassLoader classLoader, JavaModule module, boolean loaded, Throwable throwable) {
                // System.err.println("[SaarthiAgent] Error transforming " + typeName + ": " + throwable.getMessage());
            }

            @Override
            public void onComplete(String typeName, ClassLoader classLoader, JavaModule module, boolean loaded) {}
        };

        new AgentBuilder.Default()
            .disableClassFormatChanges()
            .with(AgentBuilder.RedefinitionStrategy.RETRANSFORMATION)
            .with(listener)
            .ignore(ElementMatchers.nameStartsWith("net.bytebuddy.")
                    .or(ElementMatchers.nameStartsWith("org.jacoco."))
                    .or(ElementMatchers.nameStartsWith("com.saarthi.agent.")))

            // HTTP Request/Response (javax and jakarta)
            .type(ElementMatchers.hasSuperType(ElementMatchers.named("javax.servlet.http.HttpServlet")
                    .or(ElementMatchers.named("jakarta.servlet.http.HttpServlet"))))
            .transform((builder, typeDescription, classLoader, module, protectionDomain) ->
                builder.visit(Advice.to(HttpAdvice.class).on(ElementMatchers.named("service"))))

            // Spring DispatcherServlet
            .type(ElementMatchers.named("org.springframework.web.servlet.DispatcherServlet"))
            .transform((builder, typeDescription, classLoader, module, protectionDomain) ->
                builder.visit(Advice.to(SpringMvcAdvice.class).on(ElementMatchers.named("doService").or(ElementMatchers.named("doDispatch")))))

            // JDBC Connection (to capture SQL for PreparedStatement)
            .type(ElementMatchers.hasSuperType(ElementMatchers.named("java.sql.Connection")))
            .transform((builder, typeDescription, classLoader, module, protectionDomain) ->
                builder.visit(Advice.to(JdbcConnectionAdvice.class).on(ElementMatchers.named("prepareStatement").or(ElementMatchers.named("prepareCall")))))

            // JDBC PreparedStatement
            .type(ElementMatchers.hasSuperType(ElementMatchers.named("java.sql.PreparedStatement")))
            .transform((builder, typeDescription, classLoader, module, protectionDomain) ->
                builder.visit(Advice.to(JdbcPreparedStatementAdvice.class).on(ElementMatchers.nameStartsWith("execute"))))

            // JDBC Statement (excluding PreparedStatements to avoid double reporting)
            .type(ElementMatchers.hasSuperType(ElementMatchers.named("java.sql.Statement"))
                    .and(ElementMatchers.not(ElementMatchers.hasSuperType(ElementMatchers.named("java.sql.PreparedStatement")))))
            .transform((builder, typeDescription, classLoader, module, protectionDomain) ->
                builder.visit(Advice.to(JdbcStatementAdvice.class).on(ElementMatchers.nameStartsWith("execute")
                    .and(ElementMatchers.takesArguments(String.class, int.class).or(ElementMatchers.takesArguments(String.class, int[].class)).or(ElementMatchers.takesArguments(String.class, String[].class)).or(ElementMatchers.takesArguments(String.class))))))

            // Filesystem
            .type(ElementMatchers.named("java.io.FileInputStream").or(ElementMatchers.named("java.io.FileOutputStream")))
            .transform((builder, typeDescription, classLoader, module, protectionDomain) ->
                builder.visit(Advice.to(FilesystemAdvice.class).on(ElementMatchers.isConstructor().and(ElementMatchers.takesArgument(0, java.io.File.class).or(ElementMatchers.takesArgument(0, String.class))))))

            // Command Execution
            .type(ElementMatchers.named("java.lang.ProcessBuilder"))
            .transform((builder, typeDescription, classLoader, module, protectionDomain) ->
                builder.visit(Advice.to(ProcessBuilderAdvice.class).on(ElementMatchers.named("start"))))

            .installOn(inst);

        // Schedule periodic summary
        Thread summaryThread = new Thread(() -> {
            while (true) {
                try {
                    Thread.sleep(10000);
                    printSummary();
                } catch (InterruptedException e) {
                    break;
                }
            }
        });
        summaryThread.setDaemon(true);
        summaryThread.start();

        printSummary();
        System.out.println("[SaarthiAgent] Instrumentation initialized successfully.");
    }

    private static void printSummary() {
        System.out.println("\n================================================");
        System.out.println("Saarthi Runtime Instrumentation");
        System.out.println("Servlet Provider    : " + (servletDetected.get() ? "Detected (Javax/Jakarta)" : "Monitoring..."));
        System.out.println("HTTP Hooks          : Active");
        System.out.println("Spring MVC Hooks    : " + (springDetected.get() ? "Active (Detected)" : "Monitoring..."));
        System.out.println("JDBC Hooks          : " + (jdbcDetected.get() ? "Active (Detected)" : "Monitoring..."));
        System.out.println("Filesystem Hooks    : Active");
        System.out.println("Process Hooks       : Active");
        System.out.println("Transformed Classes : " + transformedClassesCount.get());
        System.out.println("Endpoint            : " + EventPublisher.getAdapterUrl());
        System.out.println("================================================\n");
    }

    public static class HttpAdvice {
        @Advice.OnMethodEnter
        public static void onEnter(@Advice.Argument(0) Object request) {
            try {
                Method getMethod = request.getClass().getMethod("getMethod");
                Method getUri = request.getClass().getMethod("getRequestURI");
                String method = (String) getMethod.invoke(request);
                String uri = (String) getUri.invoke(request);

                Map<String, Object> attrs = new HashMap<>();
                attrs.put("method", method);
                attrs.put("uri", uri);
                EventPublisher.publish("http_request", attrs);
            } catch (Throwable t) {}
        }

        @Advice.OnMethodExit(onThrowable = Throwable.class)
        public static void onExit(@Advice.Argument(1) Object response) {
            try {
                Method getStatus = response.getClass().getMethod("getStatus");
                int status = (Integer) getStatus.invoke(response);

                Map<String, Object> attrs = new HashMap<>();
                attrs.put("status", status);
                EventPublisher.publish("http_response", attrs);
            } catch (Throwable t) {}
        }
    }

    public static class SpringMvcAdvice {
        @Advice.OnMethodEnter
        public static void onEnter(@Advice.Argument(0) Object request) {
             try {
                Method getMethod = request.getClass().getMethod("getMethod");
                Method getUri = request.getClass().getMethod("getRequestURI");
                String method = (String) getMethod.invoke(request);
                String uri = (String) getUri.invoke(request);

                Map<String, Object> attrs = new HashMap<>();
                attrs.put("framework", "spring_mvc");
                attrs.put("method", method);
                attrs.put("uri", uri);
                EventPublisher.publish("http_request", attrs);
            } catch (Throwable t) {}
        }
    }

    public static class JdbcConnectionAdvice {
        @Advice.OnMethodExit
        public static void onExit(@Advice.Argument(0) String sql, @Advice.Return Object statement) {
            if (statement != null && sql != null) {
                SaarthiAgent.preparedStatementSqlMap.put(statement, sql);
            }
        }
    }

    public static class JdbcPreparedStatementAdvice {
        @Advice.OnMethodEnter
        public static void onEnter(@Advice.This Object statement) {
            try {
                String sql = SaarthiAgent.preparedStatementSqlMap.get(statement);
                Map<String, Object> attrs = new HashMap<>();
                attrs.put("type", "prepared_statement");
                attrs.put("sql", sql != null ? sql : "UNKNOWN");
                attrs.put("class", statement.getClass().getName());
                EventPublisher.publish("database_query", attrs);
            } catch (Throwable t) {}
        }
    }

    public static class JdbcStatementAdvice {
        @Advice.OnMethodEnter
        public static void onEnter(@Advice.Argument(0) Object sqlArg) {
            try {
                if (sqlArg instanceof String) {
                    Map<String, Object> attrs = new HashMap<>();
                    attrs.put("type", "statement");
                    attrs.put("sql", (String) sqlArg);
                    EventPublisher.publish("database_query", attrs);
                }
            } catch (Throwable t) {}
        }
    }

    public static class FilesystemAdvice {
        @Advice.OnMethodEnter
        public static void onEnter(@Advice.Argument(0) Object arg) {
            try {
                Map<String, Object> attrs = new HashMap<>();
                attrs.put("path", arg.toString());
                EventPublisher.publish("filesystem_access", attrs);
            } catch (Throwable t) {}
        }
    }

    public static class ProcessBuilderAdvice {
        @Advice.OnMethodEnter
        public static void onEnter(@Advice.This Object processBuilder) {
            try {
                java.lang.ProcessBuilder pb = (java.lang.ProcessBuilder) processBuilder;
                Map<String, Object> attrs = new HashMap<>();
                attrs.put("command", pb.command().toString());
                EventPublisher.publish("process_execution", attrs);
            } catch (Throwable t) {}
        }
    }
}
