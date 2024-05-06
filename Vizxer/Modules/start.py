import random
from html import escape

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler

from Vizxer import application, db
from Vizxer import pm_users as collection
from Vizxer import SUPPORT_CHAT, SUPPORT_CHAT as SUPPORT_CHANNEL, BOT_USERNAME, CHARA_CHANNEL_ID as LOGGER_ID

OWNER_USERNAME = "tanjiro_x_coder"

IMG_URL = [
    "https://telegra.ph/file/d1f294924efee2878bfab.jpg",
    "https://telegra.ph/file/f8d968800cfd9fcf8dc81.jpg",
    "https://telegra.ph/file/d9a754538b65191932da1.jpg"
]

async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name
    username = update.effective_user.username

    user_data = await collection.find_one({"_id": user_id})

    if user_data is None:
        await collection.insert_one({"_id": user_id, "first_name": first_name, "username": username})
        await context.bot.send_message(chat_id=LOGGER_ID,
                                       text=f"New user Started The Bot..\n User: <a href='tg://user?id={user_id}'>{escape(first_name)}</a>",
                                       parse_mode='HTML')
    else:
        if user_data['first_name'] != first_name or user_data['username'] != username:
            await collection.update_one({"_id": user_id}, {"$set": {"first_name": first_name, "username": username}})

    if update.effective_chat.type == "private":
        caption = f"""
🦋 ɢʀᴇᴇᴛɪɴɢs {first_name}, ɪ'ᴍ {BOT_USERNAME}, ɴɪᴄᴇ ᴛᴏ ᴍᴇᴇᴛ ʏᴏᴜ!💞
▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰
⌥ ᴡʜᴀᴛ ᴄᴀɴ ɪ ᴅᴏ ? 🤔
▸ ɪ ᴄᴀɴ sᴘᴀᴡɴ ᴡᴀɪғᴜs ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴄʜᴀᴛs ғᴏʀ ɢʀᴏᴜᴘ ᴄʜᴀᴛ ᴜsᴇʀs ᴛᴏ ᴀᴛᴛᴀɪɴ ᴛʜᴇᴍ. 😍
⌥ ʜᴏᴡ ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴍᴇ ? 🧐
▸ ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴄʜᴀᴛs ᴀɴᴅ ᴄʟɪᴄᴋ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ғᴏʀ ᴍᴏʀᴇ ᴅᴇᴛᴀɪʟs. 🤗
▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰
"""
        keyboard = [
            [InlineKeyboardButton("ADD ME", url=f'http://t.me/{BOT_USERNAME}?startgroup=new')],
            [InlineKeyboardButton("SUPPORT", url=f'https://t.me/{SUPPORT_CHAT}'),
             InlineKeyboardButton("UPDATES", url=f'https://t.me/{SUPPORT_CHANNEL}')],
            [InlineKeyboardButton("HELP", callback_data='help')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        photo_url = random.choice(IMG_URL)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_url, caption=caption, reply_markup=reply_markup, parse_mode='markdown')

    else:
        photo_url = random.choice(IMG_URL)
        keyboard = [
            [InlineKeyboardButton("ADD ME", url=f'http://t.me/{BOT_USERNAME}?startgroup=new')],
            [InlineKeyboardButton("SUPPORT", url=f'https://t.me/{SUPPORT_CHAT}'),
             InlineKeyboardButton("UPDATES", url=f'https://t.me/{SUPPORT_CHANNEL}')],
            [InlineKeyboardButton("HELP", callback_data='help')]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_url, caption="🎴Alive!?... \n connect to me in PM For more information ",reply_markup=reply_markup)

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
        🦋 ɢʀᴇᴇᴛɪɴɢs {first_name}, ɪ'ᴍ {BOT_USERNAME}, ɴɪᴄᴇ ᴛᴏ ᴍᴇᴇᴛ ʏᴏᴜ!💞
        ▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰
        ⌥ ᴡʜᴀᴛ ᴄᴀɴ ɪ ᴅᴏ ? 🤔
        ▸ ɪ ᴄᴀɴ sᴘᴀɴ ᴡᴀɪғᴜs ɪɴ ʏᴏᴜʀ ᴄʜᴀᴛs ғᴏʀ ɢʀᴏᴜᴘ ᴄʜᴀᴛ ᴜsᴇʀs ᴛᴏ ᴀᴛᴛᴀɪɴ ᴛʜᴇᴍ. 😍
        ⌥ ʜᴏᴡ ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴍᴇ ? 🧐
        ▸ ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴄʜᴀᴛs ᴀɴᴅ ᴄʟɪᴄᴋ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ғᴏʀ ᴍᴏʀᴇ ᴅᴇᴛᴀɪʟs. 🤗
        ▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰
        """

        keyboard = [
            [InlineKeyboardButton("ADD ME", url=f'http://t.me/{BOT_USERNAME}?startgroup=new')],
            [InlineKeyboardButton("SUPPORT", url=f'https://t.me/{SUPPORT_CHAT}'),
             InlineKeyboardButton("UPDATES", url=f'https://t.me/{SUPPORT_CHANNEL}')],
            [InlineKeyboardButton("HELP", callback_data='help')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.edit_message_caption(chat_id=update.effective_chat.id, message_id=query.message.message_id, caption=caption, reply_markup=reply_markup, parse_mode='markdown')

application.add_handler(CallbackQueryHandler(button, pattern='^help$|^back$', block=False))
start_handler = CommandHandler('start', start, block=False)
application.add_handler(start_handler)
