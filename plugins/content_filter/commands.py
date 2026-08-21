from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING

from . import handlers

if TYPE_CHECKING:
    from .plugin import ContentFilterPlugin


def register_commands(plugin: "ContentFilterPlugin"):
    plugin.command_manager.add_command(
        name="فیلتر",
        handler=partial(handlers.filter_command, plugin),
        permission="admin",
        chat_type="group",
        plugin=plugin,
    )
    plugin.command_manager.add_command(
        name="ب",
        handler=partial(handlers.filter_list_command, plugin),
        permission="admin",
        chat_type="group",
        plugin=plugin,
    )