async def filter_command(plugin, event):
    text = event.raw_text.strip()

    word = text[len("!فیلتر "):].strip()

    if not word:
        return

    plugin.word_filter.add(word)

    await event.reply(
        f"کلمه «{word}» به لیست فیلتر اضافه شد."
    )


async def filter_message(plugin, event):
    if plugin.word_filter.contains(event.raw_text):
        await event.delete()