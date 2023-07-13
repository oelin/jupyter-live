from src.commands import WatchCommand
from cleo.application import Application


application = Application()
application.add(WatchCommand())
