import asyncio

from app import bot, db, api, ctx

from vkbottle.bot import Message
from vkbottle import VKAPIError

from config.secret import first_admin_id, second_admin_id, developer_id, group_id
from misc.states import Sendall, Sendall_sub, NONE_USER, StatesClass as sc, InfoPost as IP
from misc.markup import admin_kb, take_task_kb, info_kb

@bot.on.message(text='Получить пользователей')
async def get_users(message: Message):
    if message.from_id in [first_admin_id, second_admin_id, developer_id]:
        for i in db.get_users():
            await message.answer(i)
    else:
        await message.answer('Вы не администратор.')


@bot.on.message(lev='-sendall')
async def sendall(message: Message):
    if message.from_id in [first_admin_id, second_admin_id, developer_id]:
        await bot.state_dispenser.set(message.peer_id, Sendall.MESSAGE_TEXT)
        return 'Введите текст'
    else:
        return 'Вы не являетесь администратором'
    
@bot.on.message(state=Sendall.MESSAGE_TEXT)
async def sendall_handler(message: Message):
    await bot.state_dispenser.delete(message.peer_id)
    asyncio.run(await sendall_func(message))


async def sendall_func(message: Message):
    curent_offset = 0

    while True:
       
            conversations = await api.messages.get_conversations(group_id=group_id, offset=curent_offset)
            
            curent_offset += 20
            if conversations.items == []:
                return
            for con in conversations.items:
                try:
                    peer_id = con.conversation.peer.id
                    await api.messages.send(peer_id=peer_id, message=message.text, random_id=0)
                    
                except VKAPIError as ex:
                    print(ex)
                    continue
                except Exception as ex:
                    print(ex)


@bot.on.message(lev='-sendall_subs')
async def send_all_subs(message: Message):
        if message.from_id in [first_admin_id, second_admin_id, developer_id]:
            await bot.state_dispenser.set(message.peer_id, Sendall_sub.MESSAGE_TEXT)
            return 'Введите текст'
        else:
            await message.answer('Вы не являетесь администратором')



@bot.on.message(state=Sendall_sub.MESSAGE_TEXT)
async def sendall_subs_handler(message: Message):
    for user_id in db.get_users_id():
        await api.messages.send(user_id, random_id=0, message=message.text)
        await asyncio.sleep(1)
    await bot.state_dispenser.delete(message.peer_id())


@bot.on.message(lev='-delete-users')
async def delete_users_from_db(message: Message):
    if message.from_id in [first_admin_id, second_admin_id, developer_id]:
        await bot.state_dispenser.set(message.peer_id, NONE_USER.MESSAGE_TEXT)
        return 'Введите список id пользователей, которых нужно удалить через пробел (241241 12040 242112)'
    
@bot.on.message(state=NONE_USER.MESSAGE_TEXT)
async def delete_users_procces(message: Message):
    await bot.state_dispenser.delete(message.peer_id)
    users_list = message.text.strip().split()
    for user in users_list:
        try:
            db.delete_data(user)
        except:
            await message.answer(f'Пользователь с id {user} не найден')
    return 'Все указанные пользователи успешно удаленны!'

@bot.on.message(lev='/info')
async def info_handler(message: Message):
    if message.from_id in [first_admin_id, second_admin_id, developer_id]:
        await bot.state_dispenser.set(message.peer_id, IP.POST)
        return 'Введите информацию, которую нужно разослать'
    else:
        await message.answer('Вы не являетесь администратором')

@bot.on.message(state=IP.POST)
async def info_send(message: Message):
    ctx['info_id'] = message.id
    await bot.api.messages.send(user_id=message.from_id, random_id=0, forward_messages=message.id, keyboard=info_kb)
    await bot.state_dispenser.delete(message.peer_id)


@bot.on.message(lev="/post")
async def reg_handler(message: Message):
    if message.from_id in [first_admin_id, second_admin_id, developer_id]:
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