import time
import rich

from typing import ValuesView
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os.path


class Watcher:

    def __init__(self, path: str) -> None:
        if not os.path.isdir(path):
            raise ValueError(f"{path} is not a directory")
        self.path = path
        self._run = None
        self.observer = Observer()
        

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.path, recursive=False)
        self._run = True
        self.observer.start()
        try:
            while self._run:
                time.sleep(5)
        except:
            rich.print( "Error")
        finally:
            self.observer.stop()

        self.observer.join()
    
    def stop(self):
        self._run = False;


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            rich.print(f"Received created event - {event.src_path}.")

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            rich.print(f"Received modified event - {event.src_path}.")