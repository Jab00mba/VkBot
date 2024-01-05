import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import re
import time

data = []
trigger_words = ['Микронаушник', 'микронаушник', 'микро ', 'Микро ', 'Мпкронаушник', 'мпкронаушник', 'мпкро', 'Мпкро',
                 'Сдает микр', 'сдает микр']
no_trigger_words = ['Продам', 'Продам ', 'продам', 'продам', ]
seller_id = 151816656

# 'vk1.a.ZSM_bHpHG5ZCGYuDUtI_LfUOJi6kqwOeeodHNoTGQ4xBnge1N0cKRFmafoUu5EebejM6uRFaHIn0z1zRI_pR6synM9dVydVkiGmJfyhQdnBxvgaW41j1QwBNJx9wl0oKrFsv4ZpX5mqTTVlJlfwvGUUzUYEBBi47g4P3xI6mLsBwOe-T53dTUstoouXdzD0VSTcPOgc4luhvi0fHomSBPw'
my_token = 'vk1.a.6RlSi1v7leGEg_9L-3e9NS4kdthVuCWZD0Z3yrSv7lV8k0olvnZUHVzhGBgwTiegsCkUtpljEC4P4a1mMrehbJ2iYx4gYYsVaFFtGUolWs20ZrdW73PDvWxZjqstmePL2kDzJBJEuun-sVflnTLS8kLdbn0fWx435SJ1Uk88yYv4kW-R4CgJFB8Ng2NoVXqBuc7dXblkRDGdHr2DeHLaJQ'


session = vk_api.VkApi(token=my_token)
vk = session.get_api()
longpoll = VkLongPoll(session)


def send_message(id, text, msg=0, rmsg=0, is_chat=0):
    if is_chat:
        if msg:
            vk.messages.send(chat_id=id, forward_messages=msg, message=text, random_id=0)
            return 0
        vk.messages.send(chat_id=id, reply_to=rmsg, message=text, random_id=0)
        return 0
    if msg:
        vk.messages.send(user_id=id, forward_messages=msg, message=text, random_id=0)
        return 0
    vk.messages.send(user_id=id, reply_to=rmsg, message=text, random_id=0)
    return 0

def start_message():
    send_message(event.user_id, '''Привет 👋
            Сдаю Bluetooth микронаушник за 699 🔥🔥рублей с кнопкой пищалкой, обладающей функцией перезвона на последний звонок
            В КОМПЛЕКТЕ КАПСУЛЬНЫЙ И МАГНИТНЫЙ ДИНАМИК, МОЖЕШЬ ИСПОЛЬЗОВАТЬ КАКОЙ ЗАХОЧЕШЬ''')
    send_message(event.user_id, '''❕️Если Вам не отвечают на другие вопросы, подождите еще немного🤏🏽
        С Вами свяжутся в самое ближайшее время''')


def chat_message_founded(chatid):
    send_message(seller_id, f"Написал в группе '{chatid['title']}' по поводу микронаушника", msg=event.message_id)
    start_message()
    send_message(event.chat_id, "Об аренде микронаушника пишите: @micro_3ar", rmsg=event.message_id, is_chat=1)


def private_message_founded():
    start_message()
    send_message(seller_id, "Написал в ЛС по поводу микронаушника", msg=event.message_id)



for event in longpoll.listen():
    time.sleep(1)
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        if re.findall(r'|'.join(trigger_words),
                      event.text) or event.text == 'Микро' or event.text == 'микро' and not re.findall(
                r'|'.join(no_trigger_words), event.text):
            if event.from_user and event.user_id != 151816656:
                private_message_founded()
            elif event.from_chat:
                chatik = vk.messages.getChat(chat_id=event.chat_id)
                chat_message_founded(chatik)
