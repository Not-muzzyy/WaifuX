import importlib
import time
import random
import re
import asyncio
from html import escape 

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, filters

from Vizxer import collection, top_global_groups_collection, group_user_totals_collection, user_collection, user_totals_collection, shivuu
from Vizxer import application, SUPPORT_CHAT, UPDATE_CHAT, db, LOGGER
from Vizxer.Modules import ALL_MODULES


locks = {}
message_counters = {}
spam_counters = {}
last_characters = {}
sent_characters = {}
first_correct_guesses = {}
message_counts = {}


for module_name in ALL_MODULES:
    imported_module = importlib.import_module("Vizxer.Modules." + module_name)


last_user = {}
warned_users = {}
def escape_markdown(text):
    escape_chars = r'\*_`\\~>#+-=|{}.!'
    return re.sub(r'([%s])' % re.escape(escape_chars), r'\\\1', text)


async def message_counter(update: Update, context: CallbackContext) -> None:
    chat_id = str(update.effective_chat.id)
    user_id = update.effective_user.id

    if chat_id not in locks:
        locks[chat_id] = asyncio.Lock()
    lock = locks[chat_id]

    async with lock:
        
        chat_frequency = await user_totals_collection.find_one({'chat_id': chat_id})
        if chat_frequency:
            message_frequency = chat_frequency.get('message_frequency', 100)
        else:
            message_frequency = 100

        
        if chat_id in last_user and last_user[chat_id]['user_id'] == user_id:
            last_user[chat_id]['count'] += 1
            if last_user[chat_id]['count'] >= 10:
            
                if user_id in warned_users and time.time() - warned_users[user_id] < 600:
                    return
                else:
                    
                    await update.message.reply_text(f"⚠️ ᴅᴏɴ'ᴛ sᴘᴀᴍ ʙᴀᴋᴀ ! {update.effective_user.first_name}...\nᴄᴀᴜᴛɪᴏɴ:- ʏᴏᴜʀ ᴍᴇssᴀɢᴇ ᴡɪʟʟ ʙᴇ ɪɢɴᴏʀᴇᴅ ғᴏʀ 10ᴍɪɴs ʙʏ ʙᴏᴛ")
                    warned_users[user_id] = time.time()
                    return
        else:
            last_user[chat_id] = {'user_id': user_id, 'count': 1}

    
        if chat_id in message_counts:
            message_counts[chat_id] += 1
        else:
            message_counts[chat_id] = 1

    
        if message_counts[chat_id] % message_frequency == 0:
            await send_image(update, context)
            
            message_counts[chat_id] = 0
            
async def send_image(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id

    all_characters = list(await collection.find({}).to_list(length=None))
    
    if chat_id not in sent_characters:
        sent_characters[chat_id] = []

    if len(sent_characters[chat_id]) == len(all_characters):
        sent_characters[chat_id] = []

    character = random.choice([c for c in all_characters if c['id'] not in sent_characters[chat_id]])

    sent_characters[chat_id].append(character['id'])
    last_characters[chat_id] = character

    if chat_id in first_correct_guesses:
        del first_correct_guesses[chat_id]

    await context.bot.send_photo(
        chat_id=chat_id,
        photo=character['img_url'],
        caption=f"""𝗔 𝗡𝗲𝘄 𝗪𝗮𝗶𝗳𝘂:- {character['rarity']} 𝗛𝗮𝘀 𝗕𝗲𝗲𝗻 𝗔𝗽𝗽𝗲𝗮𝗿𝗲𝗱\n/attain  Mʏ ɴᴀᴍᴇ ᴀɴᴅ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ʜᴀʀᴇᴍ sᴇɴᴘᴀɪ""",
        parse_mode='Markdown')


async def guess(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    if chat_id not in last_characters:
        return

    if chat_id in first_correct_guesses:
        await update.message.reply_text(f'❌️ Tʜɪs ᴡᴀɪғᴜ ʜᴀs ᴀʟʀᴇᴀᴅʏ ʙᴇᴇɴ ᴏʙᴛᴀɪɴᴇᴅ ʏᴏᴜʀ ʟᴀᴛᴇ ᴍᴀɪɴᴛᴀɪɴ ʏᴏᴜʀ sᴘᴇᴇᴅ ʙᴀᴋᴀ !')
        return

    guess = ' '.join(context.args).lower() if context.args else ''
    
    if "()" in guess or "&" in guess.lower():
        await update.message.reply_text("Bᴀᴋᴀ ᴅᴏɴ'ᴛ ᴜsᴇ ᴛʜɪs ᴡᴏʀᴅs ᴛᴏ ᴏʙᴛᴀɪɴ")
        return


    name_parts = last_characters[chat_id]['name'].lower().split()

    if sorted(name_parts) == sorted(guess.split()) or any(part == guess for part in name_parts):

    
        first_correct_guesses[chat_id] = user_id
        
        user = await user_collection.find_one({'id': user_id})
        if user:
            update_fields = {}
            if hasattr(update.effective_user, 'username') and update.effective_user.username != user.get('username'):
                update_fields['username'] = update.effective_user.username
            if update.effective_user.first_name != user.get('first_name'):
                update_fields['first_name'] = update.effective_user.first_name
            if update_fields:
                await user_collection.update_one({'id': user_id}, {'$set': update_fields})
            
            await user_collection.update_one({'id': user_id}, {'$push': {'characters': last_characters[chat_id]}})
      
        elif hasattr(update.effective_user, 'username'):
            await user_collection.insert_one({
                'id': user_id,
                'username': update.effective_user.username,
                'first_name': update.effective_user.first_name,
                'characters': [last_characters[chat_id]],
            })

        
        group_user_total = await group_user_totals_collection.find_one({'user_id': user_id, 'group_id': chat_id})
        if group_user_total:
            update_fields = {}
            if hasattr(update.effective_user, 'username') and update.effective_user.username != group_user_total.get('username'):
                update_fields['username'] = update.effective_user.username
            if update.effective_user.first_name != group_user_total.get('first_name'):
                update_fields['first_name'] = update.effective_user.first_name
            if update_fields:
                await group_user_totals_collection.update_one({'user_id': user_id, 'group_id': chat_id}, {'$set': update_fields})
            
            await group_user_totals_collection.update_one({'user_id': user_id, 'group_id': chat_id}, {'$inc': {'count': 1}})
      
        else:
            await group_user_totals_collection.insert_one({
                'user_id': user_id,
                'group_id': chat_id,
                'username': update.effective_user.username,
                'first_name': update.effective_user.first_name,
                'count': 1,
            })


    
        group_info = await top_global_groups_collection.find_one({'group_id': chat_id})
        if group_info:
            update_fields = {}
            if update.effective_chat.title != group_info.get('group_name'):
                update_fields['group_name'] = update.effective_chat.title
            if update_fields:
                await top_global_groups_collection.update_one({'group_id': chat_id}, {'$set': update_fields})
            
            await top_global_groups_collection.update_one({'group_id': chat_id}, {'$inc': {'count': 1}})
      
        else:
            await top_global_groups_collection.insert_one({
                'group_id': chat_id,
                'group_name': update.effective_chat.title,
                'count': 1,
            })


        
        keyboard = [[InlineKeyboardButton(f"~ 𝗛𝗔𝗥𝗘𝗠 ~", switch_inline_query_current_chat=f"collection.{user_id}")]]


        await update.message.reply_text(f'<b><a href="tg://user?id={user_id}">{escape(update.effective_user.first_name)}</a></b> 𝚈𝚘𝚞 𝙾𝚋𝚝𝚊𝚒𝚗𝚎𝚍 𝚊 𝙽𝚎𝚠 𝙲𝚑𝚊𝚛𝚊𝚌𝚝𝚎𝚛 ✅️ \n\n𝗡𝗔𝗠𝗘: <b>{last_characters[chat_id]["name"]}</b> \n𝗔𝗡𝗜𝗠𝗘: <b>{last_characters[chat_id]["anime"]}</b> \n𝗥𝗔𝗜𝗥𝗧𝗬: <b>{last_characters[chat_id]["rarity"]}</b>\n\nThis Character added in Your harem.. use /harem To see your harem', parse_mode='HTML', reply_markup=InlineKeyboardMarkup(keyboard))

    else:
        await update.message.reply_text('ʙᴀᴋᴀ ᴛʜᴇ ᴡᴀɪғᴜ ɴᴀᴍᴇ ɪs ᴡʀᴏɴɢ ,ᴄᴏʀʀᴇᴄᴛ ɪᴛ ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴍᴇ ᴛᴏ ʙᴇ ʏᴏᴜʀs')
   

async def fav(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id

    
    if not context.args:
        await update.message.reply_text('Please provide Character id...')
        return

    character_id = context.args[0]

    
    user = await user_collection.find_one({'id': user_id})
    if not user:
        await update.message.reply_text('ɢᴇᴇᴢ ! ɢᴏ ɢᴇᴛ ᴀᴛʟᴇᴀsᴛ ᴏɴᴇ ᴡᴀɪғᴜ ᴀɴᴅ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ')
        return


    character = next((c for c in user['characters'] if c['id'] == character_id), None)
    if not character:
        await update.message.reply_text('sᴇɴᴘᴀɪ ᴛʜɪs ᴄʜᴀʀᴀᴄᴛᴇʀ ɪs ɴᴏᴛ ɪɴ ʏᴏᴜʀ ᴄᴏʟʟᴇᴄᴛɪᴏɴs ᴍᴀʏʙᴇ sᴏᴏɴ 👀')
        return

    
    user['favorites'] = [character_id]

    
    await user_collection.update_one({'id': user_id}, {'$set': {'favorites': user['favorites']}})

    await update.message.reply_text(f'𝗪𝗮𝗶𝗳𝘂 :- {character["name"]} 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝗮𝗱𝗱𝗲𝗱 𝘁𝗼 𝘆𝗼𝘂𝗿 𝗳𝗮𝘃𝗼𝘂𝗿𝗶𝘁𝗲𝘀 ⚡')
    



def main() -> None:
    """Run bot."""

    application.add_handler(CommandHandler(["obtain", "protecc", "collect", "grab", "hunt", "attain", "get"], guess, block=False))
    application.add_handler(CommandHandler("fav", fav, block=False))
    application.add_handler(MessageHandler(filters.ALL, message_counter, block=False))

    application.run_polling(drop_pending_updates=True)
    
if __name__ == "__main__":
    shivuu.start()
    LOGGER.info("Bot started")
    main()

