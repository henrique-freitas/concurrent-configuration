from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, List, Tuple
import yaml
import logging
from .plugins import PluginManager

logger = logging.getLogger("config_validator.core")

@dataclass
class FileResult:
    path: Path
    valid: bool
    errors: List[str]
    data: Dict[str, Any]

class ConfigValidator:
    def __init__(self, directory: Path, workers: int = 6):
        self.directory = directory
        self.workers = workers
        self.plugins = PluginManager()
        # register built-in rule plugin (exists in rules module)
        from .rules import BuiltinRules
        self.plugins.register(BuiltinRules())

    def discover_files(self) -> List[Path]:
        yaml_files = []
        for root, dirs, files in __import__('os').walk(str(self.directory)):
            for f in files:
                if f.endswith(('.yml', '.yaml')):
                    yaml_files.append(Path(root) / f)
        return yaml_files

    def validate_file(self, path: Path) -> FileResult:
        errors: List[str] = []
        data = {}
        try:
            content = path.read_text(encoding='utf-8')
            data = yaml.safe_load(content) or {}
        except Exception as exc:
            logger.exception("Failed to parse YAML: %s", path)
            return FileResult(path=path, valid=False, errors=[f"YAML parse error: {exc}"], data={})

        # run plugins to validate - each plugin returns list of errors
        for plugin in self.plugins.get_plugins():
            try:
                errs = plugin.validate(data, path=path)
                if errs:
                    errors.extend(errs)
            except Exception as exc:
                logger.exception("Plugin %s raised an exception for %s", plugin, path)
                errors.append(f"Plugin error: {plugin.__class__.__name__}: {exc}")

        valid = len(errors) == 0
        return FileResult(path=path, valid=valid, errors=errors, data=data)

    def run_once(self) -> Dict[str, Any]:
        files = self.discover_files()
        results: List[FileResult] = []
        with ThreadPoolExecutor(max_workers=self.workers) as ex:
            futures = {ex.submit(self.validate_file, p): p for p in files}
            for fut in as_completed(futures):
                res = fut.result()
                results.append(res)
        # produce simple dict for reporting
        return {
            'results': results
        }
