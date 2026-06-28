package com.saarthi.agent;

import com.google.gson.Gson;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.Map;
import java.util.HashMap;

public class EventPublisher {

    private static final String ADAPTER_URL = "http://localhost:8081/events";

    // Bounded queue to prevent OOM on high throughput. Drops events if saturated.
    private static final ExecutorService executor = new ThreadPoolExecutor(
        1, 1,
        0L, TimeUnit.MILLISECONDS,
        new ArrayBlockingQueue<Runnable>(1000),
        new ThreadPoolExecutor.DiscardPolicy()
    );

    private static final Gson gson = new Gson();

    public static void publish(String eventType, Map<String, Object> attributes) {
        Map<String, Object> payload = new HashMap<>();
        payload.put("event_type", eventType);
        payload.put("attributes", attributes);

        String jsonPayload = gson.toJson(payload);

        executor.submit(() -> {
            try {
                URL url = new URL(ADAPTER_URL);
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setDoOutput(true);
                conn.setRequestMethod("POST");
                conn.setRequestProperty("Content-Type", "application/json");

                try (OutputStream os = conn.getOutputStream()) {
                    byte[] input = jsonPayload.getBytes("utf-8");
                    os.write(input, 0, input.length);
                }

                int code = conn.getResponseCode();
            } catch (Exception e) {
                // Silently drop errors to remain passive
            }
        });
    }
}
