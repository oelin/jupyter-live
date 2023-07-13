from cleo.commands.command import Command
from cleo.helpers import argument, option

from src.watcher import Watcher


class WatchCommand(Command):
    name = "watch"
    description = "Starts a jupyter-live server."
    arguments = [
        argument(
            "source",
            description="Source directory to watch.",
        ),
    ]


    def handle(self):
        source = self.argument("source")
        watcher = Watcher(source)
        watcher.run()
