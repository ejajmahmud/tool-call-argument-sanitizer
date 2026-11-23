"""Core Tool Call Argument Sanitizer implementation."""
import re
from typing import Dict, Any, List, Optional, Tuple

class SanitizationResult:
    def __init__(self, sanitized_args: Dict[str, Any], modified_keys: List[str], dropped_keys: List[str]):
        self.sanitized_args = sanitized_args
        self.modified_keys = modified_keys
        self.dropped_keys = dropped_keys

class ToolCallSanitizer:
    DANGEROUS_PATTERNS = [
        re.compile(r"\.\./"),                 # Path traversal
        re.compile(r"[;&|`$><]"),              # Shell command injection
        re.compile(r"(--|/\*|\*/|;\s*DROP)", re.IGNORECASE)  # SQL injection
    ]

    @classmethod
    def sanitize(cls, raw_args: Dict[str, Any], schema_properties: Dict[str, Any]) -> SanitizationResult:
        sanitized = {}
        modified = []
        dropped = []

        for k, v in raw_args.items():
            if k not in schema_properties:
                dropped.append(k)
                continue

            expected_type = schema_properties[k].get("type")
            clean_val, was_mod = cls._clean_value(v, expected_type)
            sanitized[k] = clean_val
            if was_mod:
                modified.append(k)

        return SanitizationResult(sanitized, modified, dropped)

    @classmethod
    def _clean_value(cls, val: Any, expected_type: Optional[str]) -> Tuple[Any, bool]:
        modified = False

        # Type coercion
        if expected_type == "integer" and not isinstance(val, int):
            try:
                val = int(val)
                modified = True
            except (ValueError, TypeError):
                val = 0
                modified = True
        elif expected_type == "number" and not isinstance(val, (int, float)):
            try:
                val = float(val)
                modified = True
            except (ValueError, TypeError):
                val = 0.0
                modified = True
        elif expected_type == "boolean" and not isinstance(val, bool):
            if str(val).lower() in ("true", "1", "yes"):
                val = True
            else:
                val = False
            modified = True

        # String sanitization
        if isinstance(val, str):
            orig = val
            for pat in cls.DANGEROUS_PATTERNS:
                val = pat.sub("", val)
            if val != orig:
                modified = True

        return val, modified
