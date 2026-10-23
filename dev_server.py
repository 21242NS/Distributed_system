import subprocess
import sys
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


WATCHED_FILES = {"Lab1/server.py", "Lab1/mandelbrot_set.py", "dev_server.py"}


class RestartOnChange(FileSystemEventHandler):
    def __init__(self, restart):
        self.restart = restart

    def on_any_event(self, event):
        if event.event_type not in {"modified", "created", "moved", "deleted"}:
            return
        source_path = Path(event.src_path)
        relative_path = str(
            source_path.relative_to(Path.cwd()) if source_path.is_absolute() else source_path
        )
        if not event.is_directory and relative_path in WATCHED_FILES:
            self.restart()


def main():
    process = None
    restarting = False

    def start():
        nonlocal process
        process = subprocess.Popen([sys.executable, "Lab1/server.py"])
        print(f"[reloader] Started server with pid {process.pid}", flush=True)

    def restart():
        nonlocal restarting
        if restarting:
            return
        restarting = True
        print("[reloader] Source changed; restarting server", flush=True)
        process.terminate()
        process.wait(timeout=10)
        start()
        restarting = False

    start()
    observer = Observer()
    observer.schedule(RestartOnChange(restart), ".", recursive=True)
    observer.start()

    try:
        while True:
            if process.poll() is not None and not restarting:
                print("[reloader] Server stopped; restarting", flush=True)
                start()
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        if process.poll() is None:
            process.terminate()
    observer.join()


if __name__ == "__main__":
    main()