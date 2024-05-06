class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    OWNER_ID = "7011799629"
    sudo_users = "6453545159", "6396361171", "6453545159", "5932230962"
    GROUP_ID = -1002145420408
    TOKEN = "6814319101:AAGvl3ZJWVp_msQmJKg5ZxsQs4gTViXeHy0"
    mongo_url = "mongodb+srv://edit72160:edit72160@cluster0.aceg9xy.mongodb.net/?retryWrites=true&w=majority"
    PHOTO_URL = ["https://telegra.ph/file/b8232e33e2e1d09c5687f.jpg", "https://telegra.ph/file/4211fb191383d895dab9d.jpg"]
    SUPPORT_CHAT = "Rulers_Bots_Support"
    UPDATE_CHAT = "Rulers_Bots"
    BOT_USERNAME = "Attain_Your_Waifu_Bot"
    CHARA_CHANNEL_ID = "-1002145420408"
    api_id = 19869418
    api_hash = "c69a930758c50d764ad678b84c097a55"

    
class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
