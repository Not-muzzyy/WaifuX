import random
from html import escape 

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

from Vizxer import application, PHOTO_URL, SUPPORT_CHAT, UPDATE_CHAT, BOT_USERNAME, db, GROUP_ID
from Vizxer import pm_users as collection 

async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    username = update.effective_user.username

    user_data = await collection.find_one({"_id": user_id})

    if user_data is None:
        await collection.insert_one({"_id": user_id, "first_name": first_name, "username": username})
        await context.bot.send_message(chat_id=GROUP_ID, 
                                       text=f"New user Started The Bot..\n User: <a href='tg://user?id={user_id}'>{escape(first_name)})</a>", 
                                       parse_mode='HTML')
    else:
        if user_data['first_name'] != first_name or user_data['username'] != username:
            await collection.update_one({"_id": user_id}, {"$set": {"first_name": first_name, "username": username}})

    if update.effective_chat.type == "private":
        caption = f"""
        🦋 ɢʀᴇᴇᴛɪɴɢs {Name}, ɪ'ᴍ {BOT_USERNAME} , ɴɪᴄᴇ ᴛᴏ ᴍᴇᴇᴛ ʏᴏᴜ!💞\n
        ▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n
        ⌥ ᴡʜᴀᴛ ᴄᴀɴ ɪ ᴅᴏ ? 🤔\n
        ▸ ɪ ᴄᴀɴ sᴘᴀᴡɴ ᴡᴀɪғᴜs ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴄʜᴀᴛs ғᴏʀ\nɢʀᴏᴜᴘ ᴄʜᴀᴛ ᴜsᴇʀs ᴛᴏ ᴀᴛᴛᴀɪɴ ᴛʜᴇᴍ. 😍\n
        ⌥ ʜᴏᴡ ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴍᴇ ? 🧐\n
        ▸ ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴄʜᴀᴛs ᴀɴᴅ ᴄʟɪᴄᴋ ᴛʜᴇ\nғᴏʟʟᴏᴡɪɴɢ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ғᴏʀ ᴍᴏʀᴇ ᴅᴇᴛᴀɪʟs. 🤗\n
        ▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰
        """
        keyboard = [
            [InlineKeyboardButton("🪄 ᴧᴅᴅ ᴍᴇ ɪɴ ʏ𑄝ᴜꝛ ɢꝛ𑄝ᴜᴘs 🪄", url=f'http://t.me/{BOT_USERNAME}?startgroup=new')],
            [InlineKeyboardButton("✨ sᴜᴘᴘ𑄝ʀᴛ ✨", url=f'https://t.me/{SUPPORT_CHAT}'),
            InlineKeyboardButton("❄️ ᴜᴘᴅᴧᴛᴇs ❄️", url=f'https://t.me/{UPDATE_CHAT}')],
            [InlineKeyboardButton("🧿 ʜᴇʟᴘ 🧿", callback_data='help'),
            InlineKeyboardButton("👨🏻‍💻 ᴍᴧɪɴᴛᴇɴᴧɴᴇʀs 👨🏻‍💻",url=f'https://t.me/Rulers_Bots/1')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        photo_url = random.choice(PHOTO_URL)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_url, caption=caption, reply_markup=reply_markup, parse_mode='markdown')
    else:
        photo_url = random.choice(PHOTO_URL)
        keyboard = [
            [InlineKeyboardButton("🪄 ᴄ𑄝ɴɴᴇᴄᴛ ᴍᴇ ɪɴ ᴘᴍ 🪄", url=f'http://t.me/{BOT_USERNAME}?start')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        caption = f"""👋 ʜᴇʏ{first_name}, \nɪ'ᴍ ᴀʟᴡᴀʏs ᴏɴʟɪɴᴇ ғᴏʀ ʏᴏᴜ ʙᴀʙᴇ. 💕\n\n⌥ ᴄʟɪᴄᴋ ᴏɴ ғᴏʟʟᴏᴡɪɴɢ ʙᴜᴛᴛᴏɴ & ᴄᴏɴɴᴇᴄᴛ ᴍᴇ ɪɴ ᴘᴍ ғᴏʀ ᴍᴏʀᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ."""
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_url, caption=caption, reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'help':
        help_text = """
        Hᴇʟᴘ Sᴇᴄᴛɪᴏɴ:
        /attain: Tᴏ Aᴛᴛᴀɪɴ Cʜᴀʀᴀᴄᴛᴇʀ (ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs)
        /fav : Aᴅᴅ Yᴏᴜʀ Fᴀᴠ
        /trade : Tᴏ Tʀᴀᴅᴇ Cʜᴀʀᴀᴄᴛᴇʀs
        /gift : Gɪᴠᴇ Aɴʏ Cʜᴀʀᴀᴄᴛᴇʀ Fʀᴏᴍ Yᴏᴜʀ Cᴏʟʟᴇᴄᴛɪᴏɴ Tᴏ Aɴᴏᴛʜᴇʀ Usᴇʀ.. (ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs)
        /collection : Tᴏ Sᴇᴇ Yᴏᴜʀ Cᴏʟʟᴇᴄᴛɪᴏɴ
        /topgroups : Sᴇᴇ Tᴏᴘ Gʀᴏᴜᴘs Wʜᴇʀᴇ Usᴇʀs Aᴛᴛᴀɪɴs Mᴏsᴛ Iɴ Tʜᴀᴛ Gʀᴏᴜᴘ
        /top : Tᴏᴏ Sᴇᴇ Tᴏᴘ Usᴇʀs
        /ctop : Yᴏᴜʀ Cʜᴀᴛ Tᴏᴘ
        /changetime : Cʜᴀɴɢᴇ Cʜᴀʀᴀᴄᴛᴇʀ Sᴘᴀᴡɴ Tɪᴍᴇ (ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs)
        """
        help_keyboard = [[InlineKeyboardButton("⤾ Bᴀᴄᴋ", callback_data='back')]]
        reply_markup = InlineKeyboardMarkup(help_keyboard)
        
        await context.bot.edit_message_caption(chat_id=update.effective_chat.id, message_id=query.message.message_id, caption=help_text, reply_markup=reply_markup, parse_mode='markdown')

    elif query.data == 'back':
        caption = f"""
        🦋 ɢʀᴇᴇᴛɪɴɢs {first_name}, ɪ'ᴍ {BOT_USERNAME} , ɴɪᴄᴇ ᴛᴏ ᴍᴇᴇᴛ ʏᴏᴜ!💞
        ▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰
        ⌥ ᴡʜᴀᴛ ᴄᴀɴ ɪ ᴅᴏ ? 🤔
        ▸ ɪ ᴄᴀɴ sᴘᴀɴ ᴡᴀɪғᴜs ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴄʜᴀᴛs ғᴏʀ ɢʀᴏᴜᴘ ᴄʜᴀᴛ ᴜsᴇʀs ᴛᴏ ᴀᴛᴛᴀɪɴ ᴛʜᴇᴍ. 😍
        ⌥ ʜᴏᴡ ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴍᴇ ? 🧐
        ▸ ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴄʜᴀᴛs ᴀɴᴅ ᴄʟɪᴄᴋ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ғᴏʀ ᴍᴏʀᴇ ᴅᴇᴛᴀɪʟs. 🤗
        ▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰
        """
        keyboard = [
            [InlineKeyboardButton("🪄 ᴧᴅᴅ ᴍᴇ ɪɴ ʏ𑄝ᴜꝛ ɢꝛ𑄝ᴜᴘs 🪄", url=f'http://t.me/{BOT_USERNAME}?startgroup=new')],
            [InlineKeyboardButton("✨ sᴜᴘᴘ𑄝ʀᴛ ✨", url=f'https://t.me/{SUPPORT_CHAT}'),
            InlineKeyboardButton("❄️ ᴜᴘᴅᴧᴛᴇs ❄️", url=f'https://t.me/{UPDATE_CHAT}')],
            [InlineKeyboardButton("🧿 ʜᴇʟᴘ 🧿", callback_data='help'),
            InlineKeyboardButton("👨🏻‍💻 ᴍᴧɪɴᴛᴇɴᴧɴᴇʀs 👨🏻‍💻",url=f'https://t.me/Rulers_Bots/1')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.edit_message_caption(chat_id=update.effective_chat.id, message_id=query.message.message_id, caption=caption, reply_markup=reply_markup, parse_mode='markdown')

application.add_handler(CallbackQueryHandler(button, pattern='^help$|^back$', block=False))
start_handler = CommandHandler('start', start, block=False)
application.add_handler(start_handler)
