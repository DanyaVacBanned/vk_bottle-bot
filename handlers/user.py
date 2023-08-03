from app import bot, api, db
from config.secret import group_id, first_admin_id, second_admin_id, developer_id

from vkbottle.bot import Message 


from misc.utils import get_text
from misc.markup import sub_kb, unsub_kb, delete_keyboadr

@bot.on.message(text='Начать')
async def on_start(message:Message):
    await message.answer(message=get_text(), keyboard=sub_kb)

@bot.on.message(text='Подписаться на сервис')
async def subscribe(message: Message):
    if await api.groups.is_member(group_id, message.from_id):
        users_info = await bot.api.users.get(message.from_id)
        db.add_user(user_id=message.from_id, ID=message.from_id, name=f'{users_info[0].first_name} {users_info[0].last_name}')
        await message.answer(str(get_text()))
    else:
        await message.answer('Вы должны быть подписанны на группу')

@bot.on.message(text="Отписаться от сервиса")
async def unsubscribe(message: Message):
    db.delete_user(user_id=message.from_id)
    await message.answer("Вы успешно отписались от сервиса")


@bot.on.message(text='-delete_keyboard')
async def delete_keyboard(message: Message):
    await api.messages.send(peer_id=message.peer_id, random_id=0, keyboard=delete_keyboadr.get_json(), message='Клавиатура удалена')
    



