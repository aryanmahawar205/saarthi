import json
import threading
import uuid
from typing import List, Dict, Any
from http.server import HTTPServer, BaseHTTPRequestHandler
from runtime_agent.adapters.base_adapter import RuntimeAdapter
from runtime.models.runtime_event import RuntimeEvent, EventType

class JavaAgentHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)

        try:
            event_data = json.loads(post_data.decode('utf-8'))
            print(f"[JavaAdapter] Received event: {event_data.get('event_type')}")
            self.server.adapter.handle_event(event_data)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
        except Exception as e:
            print(f"[JavaAdapter] Error processing POST: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error: {e}".encode())

    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
        elif self.path == '/events':
            events = self.server.adapter.collect_events()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            # Simple conversion for verification
            event_dicts = []
            for e in events:
                event_dicts.append({
                    "event_type": e.event_type.value,
                    "attributes": e.attributes
                })
            self.wfile.write(json.dumps(event_dicts).encode())
        else:
            self.send_response(404)
            self.end_headers()

class JavaAdapterServer(HTTPServer):
    def __init__(self, server_address, RequestHandlerClass, adapter):
        super().__init__(server_address, RequestHandlerClass)
        self.adapter = adapter

class JavaAdapter(RuntimeAdapter):
    def __init__(self):
        self.events = []
        self._lock = threading.Lock()
        self.server = None
        self.server_thread = None
        self.is_running = False
        self.server_address = ('localhost', 8081) # Default address

    def initialize(self) -> None:
        pass

    def start(self) -> None:
        if self.is_running:
            return

        self.server = JavaAdapterServer(self.server_address, JavaAgentHandler, self)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        self.is_running = True
        print(f"[JavaAdapter] Started event receiver on {self.server_address}")

    def stop(self) -> None:
        if not self.is_running:
            return

        if self.server:
            self.server.shutdown()
            self.server.server_close()

        if self.server_thread:
            self.server_thread.join()

        self.is_running = False
        print("[JavaAdapter] Stopped event receiver")

    def handle_event(self, event_data: Dict[str, Any]):
        event_type_str = event_data.get("event_type")
        attributes = event_data.get("attributes", {})

        # Map string to EventType enum
        event_type = None
        try:
            event_type = EventType(event_type_str)
        except ValueError:
            # For types not strictly in the enum, map to a reasonable fallback
            event_type = EventType.FUNCTION_CALL
            attributes["original_type"] = event_type_str

        event = RuntimeEvent(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            attributes=attributes,
            metadata={"source": "java_agent"}
        )

        with self._lock:
            self.events.append(event)

    def health(self) -> bool:
        return self.is_running

    def collect_events(self) -> List[Any]:
        with self._lock:
            collected = self.events
            self.events = []
            return collected

    def collect_metadata(self) -> Dict[str, Any]:
        return {"language": "Java"}

    def capabilities(self) -> List[str]:
        return ["http_request", "http_response", "database_query", "process_execution", "filesystem_access"]
