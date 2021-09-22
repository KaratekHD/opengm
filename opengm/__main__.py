from opengm import TELEGRAM_TOKEN, BOT_NAME, LOGGER
from opengm.modules import ALL_MODULES
import importlib
from aiogram import Bot, Dispatcher, executor, types

bot = Bot(token=TELEGRAM_TOKEN)
dispatcher = Dispatcher(bot)

IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []

CHAT_SETTINGS = {}
USER_SETTINGS = {}

GDPR = []

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("opengm.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__
    LOGGER.debug("Loaded Module {}".format(imported_module.__mod_name__))
    if not imported_module.__mod_name__.lower() in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can not have two modules with the same name!")
    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__gdpr__"):
        GDPR.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

@dispatcher.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    LOGGER.debug(message.chat.type)
    """
    This handler will be called when user sends `/start` command
    """
    
    text = f"Hi {message.from_user.full_name}, my name is {BOT_NAME}!\nI'm the successor to Nemesis, and am part of the openSUSE project!\nI'm an instance of OpenGM, an open source group manager bot built in python3, using the aiogram library, and am fully opensource;\nyou can find what makes me tick [here](https://github.com/openSUSE)!\n\nFeel free to submit pull requests on GitHub!\n\nYou can find the list of available commands with /help."
    await message.reply(text, parse_mode="Markdown")

def main():
    executor.start_polling(dispatcher, skip_updates=True)
    
if __name__ == '__main__':
    main()
