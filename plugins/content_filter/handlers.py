async def filter_command(plugin, event):
    text = event.raw_text.strip()

    word = text[len("!فیلتر "):].strip()

    if not word:
        return

    group_id = event.chat_id

    await plugin.word_filter.add(group_id, word)

    await event.reply(f"کلمه «{word}» به لیست فیلتر این گروه اضافه شد.")


async def filter_message(plugin, event):
    group_id = event.chat_id

    if await plugin.word_filter.contains(group_id, event.raw_text):
        await event.delete()


async def filter_list_command(plugin, event):
    
    group_id = event.chat_id


    a=await plugin.word_filter.get_all(group_id)
    
    await event.reply(str(a))