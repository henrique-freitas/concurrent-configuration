"""Entry point for the Config Validator tool."""
from __future__ import annotations
import argparse
import logging
import sys
from pathlib import Path
from src.validator.core import ConfigValidator
from src.report import ReportWriter

logger = logging.getLogger("config_validator")
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def parse_args():
    p = argparse.ArgumentParser(description='Concurrent Configuration Deployment Validator')
    p.add_argument('--path', '-p', required=True, help='Directory to scan for YAML files')
    p.add_argument('--output', '-o', default='validation_report.json', help='Path to output JSON report')
    p.add_argument('--watch', '-w', action='store_true', help='Enable watch mode (revalidate on file changes)')
    p.add_argument('--threads', '-t', type=int, default=6, help='Number of worker threads')
    return p.parse_args()

def main():
    args = parse_args()
    base = Path(args.path)
    if not base.exists():
        logger.error("Provided path does not exist: %s", base)
        sys.exit(2)
    validator = ConfigValidator(directory=base, workers=args.threads)
    results = validator.run_once()
    writer = ReportWriter(results)
    writer.save(Path(args.output))
    writer.print_summary()
    if args.watch:
        logger.info("Starting watch mode...")
        from src.watcher import start_watch
        start_watch(base, validator, writer)

if __name__ == '__main__':
    main()
