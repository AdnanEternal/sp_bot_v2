from dataclasses import dataclass
from typing import Callable


@dataclass
class Command:
    name: str
    handler: Callable
    permission: str = "everyone"
    chat_type: str = "all"
    plugin: object = None


class CommandManager:
    def __init__(self):
        self.commands = {}

    def add_command(
        self,
        name: str,
        handler: Callable,
        permission: str = "everyone",
        chat_type: str = "all",
        plugin=None,
    ):
        command = Command(
            name=name,
            handler=handler,
            permission=permission,
            chat_type=chat_type,
            plugin=plugin,
        )

        self.commands[name] = command

    def get_command(self, name: str):
        return self.commands.get(name)

    def remove_command(self, name: str):
        self.commands.pop(name, None)

    def remove_plugin_commands(self, plugin):
        commands_to_remove = [
            name
            for name, command in self.commands.items()
            if command.plugin is plugin
        ]

        for name in commands_to_remove:
            self.remove_command(name)

    def get_all_commands(self):
        return self.commands.values()