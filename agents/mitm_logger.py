import json
import os
from mitmproxy import http
import threading
import hashlib

class TrafficLogger:
    def __init__(self, output_file):
        self.output_file = output_file
        self.lock = threading.Lock()
        self.observations = {} # Use a dict for in-memory tracking to reduce IO

        # Ensure directory exists
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)

        # Clear previous observations if any at start
        with open(self.output_file, "w") as f:
            json.dump([], f)

    def request(self, flow: http.HTTPFlow):
        self._log(flow)

    def response(self, flow: http.HTTPFlow):
        self._log(flow)

    def error(self, flow: http.HTTPFlow):
        self._log(flow)

    def _get_flow_key(self, flow: http.HTTPFlow):
        # Key based on method, URL (without query params for grouping), and query/form structure
        # to allow capturing different "types" of requests to the same endpoint
        parsed_url = flow.request.pretty_url.split('?')[0]

        # We hash the keys of query and form data to distinguish different call structures
        query_keys = sorted(list(flow.request.query.keys()))
        form_keys = sorted(list(flow.request.urlencoded_form.keys()))

        structure_hash = hashlib.md5(f"{query_keys}{form_keys}".encode()).hexdigest()[:8]

        return f"{flow.request.method}_{parsed_url}_{structure_hash}"

    def _log(self, flow: http.HTTPFlow):
        key = self._get_flow_key(flow)

        with self.lock:
            # Enhanced capture of security-relevant information
            auth_type = "None"
            auth_header = flow.request.headers.get("Authorization", "")
            if auth_header:
                if auth_header.lower().startswith("bearer "):
                    auth_type = "Bearer Token"
                elif auth_header.lower().startswith("basic "):
                    auth_type = "Basic Auth"
                else:
                    auth_type = "Other"

            # Check for trust boundary crossing (e.g., external -> internal)
            # This is a simplified heuristic
            is_external = "localhost" not in flow.request.host and "127.0.0.1" not in flow.request.host

            # Update or create observation
            observation = {
                "url": flow.request.pretty_url,
                "method": flow.request.method,
                "status_code": flow.response.status_code if flow.response else 502,
                "request_headers": dict(flow.request.headers),
                "response_headers": dict(flow.response.headers) if flow.response else {},
                "cookies": dict(flow.request.cookies),
                "query_params": dict(flow.request.query),
                "form_data": dict(flow.request.urlencoded_form),
                "redirects": flow.response.headers.get("Location", None) if flow.response else None,
                "auth_flow": {
                    "type": auth_type,
                    "present": auth_type != "None"
                },
                "trust_boundary_crossing": is_external,
                "response_metadata": {
                    "content_type": flow.response.headers.get("Content-Type", "") if flow.response else "text/html",
                    "length": len(flow.response.content) if flow.response and flow.response.content else 0,
                    "server": flow.response.headers.get("Server", "") if flow.response else ""
                }
            }

            # If we already have this flow, only update if the new one has more info (like a response)
            if key in self.observations:
                old_obs = self.observations[key]
                if old_obs['status_code'] == 502 and observation['status_code'] != 502:
                     self.observations[key] = observation
                else:
                    # Keep the one with response if available
                    pass
            else:
                self.observations[key] = observation

            # Persist to disk
            try:
                with open(self.output_file, "w") as f:
                    json.dump(list(self.observations.values()), f, indent=2)
            except Exception as e:
                print(f"[TrafficLogger] Error writing to {self.output_file}: {e}")

addons = [
    TrafficLogger("reports/runtime_observations.json")
]
