from __future__ import annotations
from typing import Protocol, List, Dict, Any
from pathlib import Path
import importlib
import logging

logger = logging.getLogger("config_validator.plugins")

class ValidationPlugin(Protocol):
    def validate(self, data: Dict[str, Any], path: Path = None) -> List[str]:
        ...

class PluginManager:
    def __init__(self):
        self._plugins = []

    def register(self, plugin: ValidationPlugin):
        logger.debug("Registering plugin %s", plugin.__class__.__name__)
        self._plugins.append(plugin)

    def get_plugins(self):
        return list(self._plugins)
