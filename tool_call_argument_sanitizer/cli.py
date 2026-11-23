"""CLI for Tool Call Argument Sanitizer."""
import argparse
import json
from .core import ToolCallSanitizer

def main():
    parser = argparse.ArgumentParser(description="Tool Call Argument Sanitizer CLI")
    parser.add_argument("--demo", action="store_true", help="Run sanitization demo")
    args = parser.parse_args()

    schema = {
        "filepath": {"type": "string"},
        "retry_count": {"type": "integer"},
        "active": {"type": "boolean"}
    }
    raw = {
        "filepath": "../../etc/passwd; rm -rf /",
        "retry_count": "5",
        "active": "true",
        "unauthorized_secret_flag": "malicious"
    }

    res = ToolCallSanitizer.sanitize(raw, schema)
    print("Raw Args:", raw)
    print("Sanitized Args:", res.sanitized_args)
    print("Modified Fields:", res.modified_keys)
    print("Dropped Unknown Fields:", res.dropped_keys)

if __name__ == "__main__":
    main()
