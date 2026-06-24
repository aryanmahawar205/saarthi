from typing import List, Optional
from runtime.models.runtime_event import RuntimeEvent, EventType

class SanitizerDetector:
    def detect(self, event: RuntimeEvent) -> bool:
        """
        Detects if an event represents a sanitization action.
        This is an abstraction layer.
        """
        # In a real IAST, this would look for calls to:
        # - OWASP ESAPI
        # - html.escape
        # - bleach.clean
        # - parameterized query construction

        # Heuristic: Check function name or attributes
        func_name = event.metadata.get("name", "").lower()
        sanitizer_keywords = ["sanitize", "escape", "encode", "validate", "filter", "clean"]

        for keyword in sanitizer_keywords:
            if keyword in func_name:
                return True

        if event.attributes.get("is_sanitized") is True:
            return True

        return False
