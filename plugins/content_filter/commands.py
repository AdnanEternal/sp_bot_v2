def register_commands(plugin):
    plugin.command_manager.add_command(
        name="فیلتر",
        handler=plugin.filter_command,
        permission="admin",
        chat_type="group",
        plugin=plugin,
    )