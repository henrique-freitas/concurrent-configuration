import tempfile
from pathlib import Path
from src.validator.core import ConfigValidator
from src.report import ReportWriter
import json

SAMPLE_OK = """service: user-api
replicas: 3
image: myregistry.com/user-api:1.4.2
env:
  DATABASE_URL: postgres://db.internal:5432/users
  REDIS_URL: redis://cache.internal:6379
"""

SAMPLE_BAD = """service: user-api
replicas: 0
image: badimageformat
env:
  db_url: something
"""

def test_validator_detects_good_and_bad(tmp_path):
    base = tmp_path / "cfgs"
    base.mkdir()
    ok = base / "ok.yaml"
    bad = base / "bad.yaml"
    ok.write_text(SAMPLE_OK)
    bad.write_text(SAMPLE_BAD)
    v = ConfigValidator(directory=base, workers=2)
    res = v.run_once()
    writer = ReportWriter(res)
    report = writer.build()
    assert len(report['valid_files']) == 1
    assert len(report['invalid_files']) == 1
    assert report['total_issues'] >= 1

def test_report_counts_registry(tmp_path):
    base = tmp_path / "cfgs2"
    base.mkdir()
    a = base / "a.yaml"
    a.write_text(SAMPLE_OK)
    v = ConfigValidator(directory=base, workers=1)
    res = v.run_once()
    writer = ReportWriter(res)
    report = writer.build()
    assert 'myregistry.com' in report['registry_counts']
