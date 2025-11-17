from pathlib import Path
from src.validator.plugins import PluginManager, ValidationPlugin

class DummyPlugin(ValidationPlugin):
    def validate(self, data, path: Path = None):
        if data.get('service') == 'bad':
            return ['dummy: service cannot be bad']
        return []

def test_plugin_manager(tmp_path):
    from src.validator.core import ConfigValidator
    base = tmp_path / 'cfg'
    base.mkdir()
    p = base / 'x.yaml'
    p.write_text('service: bad\nreplicas: 1\nimage: r/s:1')
    v = ConfigValidator(directory=base, workers=1)
    v.plugins.register(DummyPlugin())
    res = v.run_once()
    results = res['results']
    assert any(r.errors for r in results)
