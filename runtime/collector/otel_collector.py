import json
import os
from typing import List
from runtime.adapters.base import RuntimeCollector
from runtime.adapters.otel_adapter import OTelAdapter
from runtime.models.runtime_event import RuntimeEvent

class OTelFileCollector(RuntimeCollector):
    """
    A simple OTel collector that reads spans from a JSON file.
    In a real scenario, this might be a gRPC server or an HTTP endpoint.
    """
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.adapter = OTelAdapter()

    def start(self):
        print(f"[OTelFileCollector] Starting to monitor {self.filepath}")

    def stop(self):
        print(f"[OTelFileCollector] Stopped monitoring {self.filepath}")

    def collect(self) -> List[RuntimeEvent]:
        if not os.path.exists(self.filepath):
            return []

        try:
            with open(self.filepath, "r") as f:
                raw_spans = json.load(f)
            return self.adapter.translate(raw_spans)
        except Exception as e:
            print(f"[OTelFileCollector] Error collecting spans: {e}")
            return []
