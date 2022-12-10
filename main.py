from vkbottle import VKAPIError
from vkbottle import CtxStorage
from vkbottle.bot import Bot, Message
from cfg import get_api_key_for_user, get_admin_id, get_text
from vkbottle import Keyboard, KeyboardButtonColor, Text
from loguru import logger
from database import Database
from states import StatesClass as sc
from states import InfoPost as IP
from states import Sendall
from vkbottle import API
import tracemalloc
from vkbottle_types.events import GroupEventType, GroupTypes
from vkbottle_types.events.objects.group_event_objects import GroupJoinObject
from vkbottle_types.objects import CallbackGroupJoin, CallbackGroupJoinType
from vkbottle import Callback
from vkbottle.modules import json
import configparser

#Инициализация
config = configparser.ConfigParser()
config.read('config.ini')
token = config['VK']['api_key']
admin_id = config['VK']['admin_id']
bot = Bot(token=token)
api = API(token=token)
db = Database(db_file='vk_db.db')
ctx  = CtxStorage()
#------------------

tracemalloc.start()
#Клавиатура
show_tasks = Keyboard().add(Callback(label='Свободные заказы',payload={'cmd':'show_tasks'}), color=KeyboardButtonColor.POSITIVE)
take_task_kb = Keyboard(inline=True).add(Callback(label='Беру', payload={'cmd':'take_task'}),color=KeyboardButtonColor.POSITIVE)
sub_kb = Keyboard(one_time=False).add(Text('Подписаться на сервис'), color=KeyboardButtonColor.POSITIVE)
request_kb=Keyboard(inline=True).add(Text('Добавить'), color=KeyboardButtonColor.POSITIVE).add(Text('Отказать'), color=KeyboardButtonColor.NEGATIVE)
#Админка
#Админская клавиатура----------------------------------------------
admin_kb = Keyboard(one_time=True, inline=False)
admin_kb.add(Text('Разослать'), color=KeyboardButtonColor.POSITIVE)
admin_kb.add(Text('Удалить'), color=KeyboardButtonColor.NEGATIVE)
main_kb = Keyboard(one_time=False, inline=False)
main_kb.add(Text('Получить пользователей'), color=KeyboardButtonColor.POSITIVE)
info_kb = Keyboard(one_time=True).add(Text('Прислать'), color=KeyboardButtonColor.POSITIVE).add(Text('Удалить_информацию'), color=KeyboardButtonColor.NEGATIVE)
#Админские команды-----------------------------------------------
@bot.on.message(text='Получить пользователей')
async def get_users(message: Message):
    if str(message.from_id) == str(admin_id):
        for i in db.get_users():
            await message.answer(i)
    else:
        await message.answer('Вы не администратор.')
#ИВЕНТЫ--------------------------------------------------------------------------



# @bot.on.raw_event(event = GroupEventType.GROUP_JOIN, dataclass=GroupTypes.GroupJoin)
# async def join_group_handler(event: GroupTypes.GroupJoin):
#     event.object.join_type = CallbackGroupJoinType.APPROVED
#     print(event)
#     await bot.api.messages.send(
#         peer_id=event.object.user_id,
#         message=str(get_text()),
#         random_id=0,
#         keyboard=show_tasks
#     )
    
#     users_info = await bot.api.users.get(event.object.user_id)
#     print(f'{event.object.user_id} {users_info[0].first_name}')
# db.add_user(user_id=event.object.user_id, ID =event.object.user_id , name=f'{users_info[0].first_name} {users_info[0].last_name}')



@bot.on.raw_event(event=GroupEventType.GROUP_LEAVE, dataclass=GroupTypes.GroupLeave)
async def leave_group(event: GroupTypes.GroupLeave):
    await bot.api.messages.send(
        peer_id=event.object.user_id,
        message='Вы отписались от сообщества, теперь вы не будете видеть новые заказы.',
        random_id=0
    
    )
    db.delete_data(ID = event.object.user_id)



@bot.on.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=GroupTypes.MessageEvent)
async def take_task(event: GroupTypes.MessageEvent):

    try:
        if event.object.payload['cmd'] == 'take_task':
            await bot.api.messages.send_message_event_answer(
                event_id=event.object.event_id,
                peer_id=event.object.peer_id,
                user_id=event.object.user_id,
                event_data=json.dumps({"type": "open_link", "link": f"https://vk.com/im?sel={str(admin_id)}"})                   
            )
        else:
            await bot.api.messages.send_message_event_answer(
                event_id=event.object.event_id,
                peer_id=event.object.peer_id,
                user_id=event.object.user_id,
                event_data=json.dumps({"type": "open_link", "link": 'https://docs.google.com/spreadsheets/d/1SZgkhGKLR8_q_XiaE1edwx6SUQ_gh5bMFJl78-c-QDY/edit#gid=0'}))
    except VKAPIError as VE:
        print(VE)
   

#dialog_id = f'https://vk.com/im?sel={str(get_admin_id())}'


@bot.on.message(text='Начать')
async def on_start(message:Message):
    await message.answer(message='Чтобы получать заказы, подпишитесь на сервис', keyboard=sub_kb)

@bot.on.message(text='Подписаться на сервис')
async def subscribe(message: Message):
    if await api.groups.is_member('123456789',message.from_id):
        users_info = await bot.api.users.get(message.from_id)
        db.add_user(user_id=message.from_id, ID=message.from_id, name=f'{users_info[0].first_name} {users_info[0].last_name}')
        await message.answer(str(get_text()), keyboard=show_tasks)
    else:
        await message.answer('Вы должны быть подписанны на группу')
@bot.on.message(lev='/info')
async def info_handler(message: Message):
    if message.from_id == int(admin_id):
        await bot.state_dispenser.set(message.peer_id, IP.POST)
        return 'Введите информацию, которую нужно разослать'
    else:
        await message.answer('Вы не являетесь администратором')
@bot.on.message(state=IP.POST)
async def info_send(message: Message):
    ctx['info_id'] = message.id
    await bot.api.messages.send(user_id=message.from_id, random_id=0, forward_messages=message.id, keyboard=info_kb)
    await bot.state_dispenser.delete(message.peer_id)

#Стейты
@bot.on.message(lev="/post")
async def reg_handler(message: Message):
    if message.from_id == int(admin_id):
        await bot.state_dispenser.set(message.peer_id, sc.NAME)
        return "Заполните ваш пост"
    else:
        await message.answer('Вы не являетесь администратором')

@bot.on.message(state=sc.NAME)
async def name_handler(message: Message):
    ctx['message_id'] = message.id
    await bot.api.messages.send(user_id=message.from_id, random_id=0, forward_messages=message.id, keyboard=admin_kb)
    await bot.state_dispenser.delete(message.peer_id)


@bot.on.message(text='Разослать')
async def send_message(message: Message):
    message_id = ctx['message_id']
    for usr in db.get_users_id():
        await api.messages.send(user_id=usr,random_id=0,peer_id=message.peer_id, forward_messages=message_id, keyboard=take_task_kb)

@bot.on.message(text='Прислать')
async def send_message(message: Message):
    message_id = ctx['info_id']
    for usr in db.get_users_id():
        await api.messages.send(user_id=usr,random_id=0,peer_id=message.peer_id, forward_messages=message_id)

@bot.on.message(text='Удалить_информацию')
async def delete_message(message: Message):
    ctx['info_id'] = ''
    await message.answer('Запись удалена')

@bot.on.message(text='Удалить')
async def delete_message(message: Message):
    ctx['post'] = ''
    await message.answer('Запись удалена')

@bot.on.message(lev='sendall')
async def send_all_func(message: Message):
        if message.from_id == int(admin_id):
            await bot.state_dispenser.set(message.peer_id, Sendall.MESSAGE_TEXT)
            return 'Введите текст'
        else:
            await message.answer('Вы не являетесь администратором')


@bot.on.message(state=Sendall.MESSAGE_TEXT)
async def sendall_func(message: Message):
    for user_id in db.get_users_id():
        await api.messages.send(user_id, random_id=0, message=message.text)
    await bot.state_dispenser.delete(message.peer_id())
    

# @bot.on.message(text='Проверка')
# async def new_message(message: Message):
#     a =await api.groups.is_member('123456789',message.from_id)
#     print(a)


logger.remove()
#Запуск
print("Бот запущен")
bot.run_forever()
