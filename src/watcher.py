from __future__ import annotations
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileCreatedEvent
import time
import logging
from pathlib import Path

logger = logging.getLogger("config_validator.watcher")

class _ChangeHandler(FileSystemEventHandler):
    def __init__(self, validator, writer):
        self.validator = validator
        self.writer = writer

    def on_modified(self, event):
        if isinstance(event, (FileModifiedEvent, FileCreatedEvent)):
            path = Path(event.src_path)
            if path.suffix in ('.yml', '.yaml'):
                logger.info("Detected change in %s - revalidating", path)
                results = self.validator.run_once()
                self.writer.results = results
                self.writer.save(Path('validation_report.json'))
                self.writer.print_summary()

def start_watch(base_path: Path, validator, writer):
    event_handler = _ChangeHandler(validator, writer)
    observer = Observer()
    observer.schedule(event_handler, str(base_path), recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
