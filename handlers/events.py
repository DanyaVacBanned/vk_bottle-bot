from app import bot, db

from vkbottle import VKAPIError
from vkbottle_types.events import GroupEventType, GroupTypes
from vkbottle.modules import json

from config.secret import first_admin_id



@bot.on.raw_event(event=GroupEventType.GROUP_LEAVE, dataclass=GroupTypes.GroupLeave)
async def leave_group(event: GroupTypes.GroupLeave):

    db.delete_data(ID = event.object.user_id)



@bot.on.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=GroupTypes.MessageEvent)
async def take_task(event: GroupTypes.MessageEvent):

    try:
        if event.object.payload['cmd'] == 'take_task':
            await bot.api.messages.send_message_event_answer(
                event_id=event.object.event_id,
                peer_id=event.object.peer_id,
                user_id=event.object.user_id,
                event_data=json.dumps({"type": "open_link", "link": f"https://vk.com/im?sel={str(first_admin_id)}"})                   
            )
        else:
            await bot.api.messages.send_message_event_answer(
                event_id=event.object.event_id,
                peer_id=event.object.peer_id,
                user_id=event.object.user_id,
                event_data=json.dumps({"type": "open_link", "link": 'https://docs.google.com/spreadsheets/d/1SZgkhGKLR8_q_XiaE1edwx6SUQ_gh5bMFJl78-c-QDY/edit#gid=0'}))
    except VKAPIError as VE:
        print(VE)