from __future__ import annotations
from typing import Dict, Any, List
from pathlib import Path
import json
from collections import Counter
import logging

logger = logging.getLogger("config_validator.report")

def _serialize_path(p):
    return str(p) if p is not None else None

class ReportWriter:
    def __init__(self, results: Dict[str, Any]):
        self.results = results

    def build(self) -> Dict[str, Any]:
        results = self.results.get('results', [])
        out = {
            'valid_files': [],
            'invalid_files': [],
            'registry_counts': {},
            'total_issues': 0
        }
        registry_counter = Counter()
        total_issues = 0
        for r in results:
            entry = {
                'path': _serialize_path(r.path),
                'valid': r.valid,
                'errors': r.errors
            }
            if r.valid:
                out['valid_files'].append(entry)
            else:
                out['invalid_files'].append(entry)
            total_issues += len(r.errors)
            # attempt to extract registry
            img = r.data.get('image') if isinstance(r.data, dict) else None
            if img and isinstance(img, str) and '/' in img:
                registry = img.split('/')[0]
                registry_counter[registry] += 1
        out['registry_counts'] = dict(registry_counter)
        out['total_issues'] = total_issues
        return out

    def save(self, path: Path):
        payload = self.build()
        with path.open('w', encoding='utf-8') as fh:
            json.dump(payload, fh, indent=2)
        logger.info("Saved report to %s", path)

    def print_summary(self):
        payload = self.build()
        print(f"Valid files: {len(payload['valid_files'])}") 
        print(f"Invalid files: {len(payload['invalid_files'])}") 
        print(f"Registries: {payload['registry_counts']}" ) 
        print(f"Total issues: {payload['total_issues']}") 
