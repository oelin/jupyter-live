# Adapted from: https://michaelcho.me/article/using-pythons-watchdog-to-monitor-changes-to-a-source.


import os
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import nbformat as nbf

from src.converter import convert


class Watcher:

    def __init__(self, source: str = '.'):
        self.source = source
        self.observer = Observer()


    def run(self) -> None:
        handler = Handler()

        self.observer.schedule(handler, self.source, recursive=True)
        self.observer.start()

        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
            print("Observer terminated.")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event) -> None:

        if event.is_directory:
            return

        elif event.event_type == "created" or event.event_type == "modified":
            path = event.src_path

            if not path.endswith('.md'):
                return  # Ignore non-markdown files.

            # Read the modified file, convert it to a notebook and then write
            # the notebook into teh target source.

            with open(path) as file:
                markdown = file.read()
                html = convert(markdown, os.path.dirname(path))

                with open(f"{path.replace('.md', '.html')}", "w") as target:
                    target.write(html)

            print(f'Converted {path}')
