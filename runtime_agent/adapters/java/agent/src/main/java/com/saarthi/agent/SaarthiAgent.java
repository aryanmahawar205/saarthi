package com.saarthi.agent;

import net.bytebuddy.agent.builder.AgentBuilder;
import net.bytebuddy.asm.Advice;
import net.bytebuddy.matcher.ElementMatchers;

import java.lang.instrument.Instrumentation;
import java.lang.reflect.Method;
import java.util.Map;
import java.util.HashMap;

public class SaarthiAgent {

    public static void premain(String agentArgs, Instrumentation inst) {
        System.out.println("[SaarthiAgent] Initializing Java Instrumentation Provider...");

        new AgentBuilder.Default()
            .disableClassFormatChanges()
            .with(AgentBuilder.RedefinitionStrategy.RETRANSFORMATION)
            .ignore(ElementMatchers.nameStartsWith("net.bytebuddy.")
                    .or(ElementMatchers.nameStartsWith("org.jacoco."))
                    .or(ElementMatchers.nameStartsWith("com.saarthi.agent.")))

            // HTTP Request/Response
            .type(ElementMatchers.hasSuperType(ElementMatchers.named("javax.servlet.http.HttpServlet")))
            .transform((builder, typeDescription, classLoader, module, protectionDomain) ->
                builder.visit(Advice.to(HttpAdvice.class).on(ElementMatchers.named("service"))))

            // JDBC PreparedStatement
            .type(ElementMatchers.hasSuperType(ElementMatchers.named("java.sql.PreparedStatement")))
            .transform((builder, typeDescription, classLoader, module, protectionDomain) ->
                builder.visit(Advice.to(JdbcPreparedStatementAdvice.class).on(ElementMatchers.named("execute").or(ElementMatchers.named("executeQuery")).or(ElementMatchers.named("executeUpdate")))))

            // JDBC Statement
            .type(ElementMatchers.hasSuperType(ElementMatchers.named("java.sql.Statement")))
            .transform((builder, typeDescription, classLoader, module, protectionDomain) ->
                builder.visit(Advice.to(JdbcStatementAdvice.class).on(ElementMatchers.named("execute").or(ElementMatchers.named("executeQuery")).or(ElementMatchers.named("executeUpdate")))))

            // Filesystem (java.io.File, java.io.FileInputStream)
            .type(ElementMatchers.named("java.io.FileInputStream").or(ElementMatchers.named("java.io.FileOutputStream")))
            .transform((builder, typeDescription, classLoader, module, protectionDomain) ->
                builder.visit(Advice.to(FilesystemAdvice.class).on(ElementMatchers.isConstructor().and(ElementMatchers.takesArgument(0, java.io.File.class).or(ElementMatchers.takesArgument(0, String.class))))))

            // Command Execution (ProcessBuilder)
            .type(ElementMatchers.named("java.lang.ProcessBuilder"))
            .transform((builder, typeDescription, classLoader, module, protectionDomain) ->
                builder.visit(Advice.to(ProcessBuilderAdvice.class).on(ElementMatchers.named("start"))))

            .installOn(inst);

        System.out.println("[SaarthiAgent] Instrumentation Provider Initialized.");
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

    public static class JdbcPreparedStatementAdvice {
        @Advice.OnMethodEnter
        public static void onEnter(@Advice.This Object statement) {
            try {
                Map<String, Object> attrs = new HashMap<>();
                attrs.put("type", "prepared_statement");
                attrs.put("class", statement.getClass().getName());
                EventPublisher.publish("database_query", attrs);
            } catch (Throwable t) {}
        }
    }

    public static class JdbcStatementAdvice {
        @Advice.OnMethodEnter
        public static void onEnter(@Advice.Argument(0) String sql) {
            try {
                Map<String, Object> attrs = new HashMap<>();
                attrs.put("type", "statement");
                attrs.put("sql", sql);
                EventPublisher.publish("database_query", attrs);
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
