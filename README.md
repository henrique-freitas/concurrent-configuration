Concurrent Configuration Deployment Validator

A production-grade Python tool designed to discover, validate, monitor, and report on YAML-based deployment configurations.

This tool validates service definitions using a plugin-based architecture, performs parallel file processing, produces a detailed JSON report, and optionally runs in watch mode to monitor changes in real-time.

🧩 Features
✅ YAML Discovery

Recursively finds all .yaml and .yml files in a directory.

✅ Concurrent Validation

Uses ThreadPoolExecutor to process multiple configuration files simultaneously.

✅ Built-in Validation Rules

Required fields: service, image, replicas

image must match: <registry>/<service>:<version>

replicas must be an integer between 1 and 50

env keys must be UPPERCASE

✅ Plugin Architecture

Add new validation rules without modifying the core validator.
Drop-in plugin support using a simple interface.

✅ JSON Report

Produces a structured report containing:

valid files

invalid files + errors

registry usage summary

total issues

✅ Watch Mode (Optional)

Automatically re-validates on file changes using watchdog.

🛠️ Installation
1. Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

2. Install dependencies
pip install -r requirements.txt

▶️ Usage 
Single Run - Local
python -m src.main --path ./examples --output report.json

Watch Mode

(Re-runs validation when files change)

python -m src.main --path ./examples --watch

Thread Count

(Default: 6 workers)

python -m src.main --path ./examples --threads 12

🧪 Running Tests
Run all tests:
pytest -v

Generate coverage:
pytest --cov=src

🐳 Docker Support
Build the image:
make docker-build or docker build -t config-validator .

Run the validator:
make docker-run or docker run --rm -v $(pwd)/examples:/app/examples config-validator \
  python -m src.main --path /app/examples

Architecture Diagram
 ┌──────────────────────────────┐
 │          main.py             │
 │ CLI parsing, triggers run    │
 └──────────────┬──────────────┘
                │
                ▼
 ┌──────────────────────────────┐
 │       ConfigValidator        │
 │  - discovers YAML files      │
 │  - runs workers (threads)    │
 │  - calls plugins             │
 └──────────────┬──────────────┘
                │
                ▼
 ┌──────────────────────────────┐
 │   Built-in & Custom Plugins  │
 │  independent rule validators │
 └──────────────┬──────────────┘
                │
                ▼
 ┌──────────────────────────────┐
 │        ReportWriter          │
 │ creates JSON + CLI summary   │
 └──────────────────────────────┘

Future Improvements

This validator can be expanded into an internal platform automation tool.
A potential next step:

➡️ Slack bot integration

Validator runs on schedule (cron or CI pipeline)

Posts alerts to Slack if:

New invalid files appear

replicas out of range

Deprecated fields appear

Registry usage changes unexpectedly

Example Slack message:

🔔 Config Validator Alert
3 invalid YAML files detected in the last commit.
Check: #devops-config-issues

This would turn the validator into a proactive Devops guardrail for configuration drift.

📌 Notes & Design Decisions

Plugins allow easy extension without touching core logic.

ThreadPoolExecutor was chosen because IO-bound YAML parsing benefits from threading.

Watchdog enables continuous validation in real-time.

Code style follows PEP8 and SRE-friendly clarity.

Tests cover validator core, reporting, and plugin registration.

👨‍💻 Author

Henrique Freitas
Site Reliability Engineer — Devops, Cloud, Automation & Observability
