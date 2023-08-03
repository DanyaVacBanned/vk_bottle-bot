from vkbottle import Keyboard, KeyboardButtonColor, Text, Callback


#Клавиатура

take_task_kb = Keyboard(inline=True).add(Callback(label='Получить скидку', payload={'cmd':'take_task'}),color=KeyboardButtonColor.POSITIVE)
sub_kb = Keyboard(one_time=True).add(Text('Подписаться на сервис'), color=KeyboardButtonColor.POSITIVE)
unsub_kb = Keyboard(one_time=True).add(Text("Отписаться от сервиса"), color=KeyboardButtonColor.NEGATIVE)
request_kb=Keyboard(inline=True).add(Text('Добавить'), color=KeyboardButtonColor.POSITIVE).add(Text('Отказать'), color=KeyboardButtonColor.NEGATIVE)
delete_keyboadr = Keyboard(one_time=True)
#Админка
#Админская клавиатура----------------------------------------------
admin_kb = Keyboard(one_time=True, inline=False)
admin_kb.add(Text('Разослать'), color=KeyboardButtonColor.POSITIVE)
admin_kb.add(Text('Удалить'), color=KeyboardButtonColor.NEGATIVE)
main_kb = Keyboard(one_time=False, inline=False)
main_kb.add(Text('Получить пользователей'), color=KeyboardButtonColor.POSITIVE)
info_kb = Keyboard(one_time=True).add(Text('Прислать'), color=KeyboardButtonColor.POSITIVE).add(Text('Удалить_информацию'), color=KeyboardButtonColor.NEGATIVE)
