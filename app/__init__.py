
from vkbottle import CtxStorage, API
from vkbottle.bot import Bot

from misc.database.database import Database
from config.secret import token

bot = Bot(token=token)
api = API(token=token)
db = Database(db_file='vk_db.db')
ctx  = CtxStorage()