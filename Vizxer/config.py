class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    OWNER_ID = "6453545159"
    sudo_users = "7011799629", "6396361171"
    GROUP_ID = -1002145420408
    TOKEN = "6889782542:AAFfQ13Rji_eDZkysaxHeEJTWdfjsDuNPts"
    mongo_url = "mongodb+srv://ichigobotcloud:GHGfLff2QFlT4sMM@aryanzxa.0r5vjie.mongodb.net/?retryWrites=true&w=majority&appName=aryanzxa"
    PHOTO_URL = ["https://telegra.ph/file/b8232e33e2e1d09c5687f.jpg", "https://telegra.ph/file/4211fb191383d895dab9d.jpg"]
    SUPPORT_CHAT = "Rulers_Bots_Support"
    UPDATE_CHAT = "waifuobtainers"
    BOT_USERNAME = "Waifu_obtainerbot"
    CHARA_CHANNEL_ID = "-1002071072596"
    api_id = 19869418
    api_hash = "c69a930758c50d764ad678b84c097a55"

    
class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True