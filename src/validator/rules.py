from __future__ import annotations
from typing import Dict, Any, List
from pathlib import Path
import re
from .plugins import ValidationPlugin

class BuiltinRules(ValidationPlugin):
    REQUIRED_KEYS = ['service', 'image', 'replicas']

    def validate(self, data: Dict[str, Any], path: Path = None) -> List[str]:
        errors: List[str] = []
        # required keys
        for key in self.REQUIRED_KEYS:
            if key not in data:
                errors.append(f"missing required key: {key}")
        # replicas
        if 'replicas' in data:
            try:
                val = int(data['replicas'])
                if not (1 <= val <= 50):
                    errors.append("replicas must be integer between 1 and 50")
            except Exception:
                errors.append("replicas must be an integer")
        # image pattern <registry>/<service>:<version>
        if 'image' in data:
            pattern = r'^[\w.-]+\/.+:.*$'
            if not re.match(pattern, str(data['image'])):
                errors.append("image must follow <registry>/<service>:<version>")
        # env uppercase keys
        if 'env' in data and isinstance(data['env'], dict):
            for k in data['env'].keys():
                if not k.isupper():
                    errors.append(f"env key '{k}' must be uppercase")
        return errors
