# Concurrent Configuration Deployment Validator

A lightweight Python tool to discover, validate and monitor YAML deployment configuration files.
Implements plugin-based validations, concurrent processing, JSON reporting and optional --watch mode.

## Quickstart

1. Create a virtualenv and install requirements:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the validator:
```bash
python -m src.main --path ./examples --output report.json
```

3. Watch mode:
```bash
python -m src.main --path ./examples --watch
```
