#!/bin/python3
import json
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import requests
from db import *
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
def send(message,tok,peer_id,reply=None):
    return json.loads(requests.post("https://api.vk.com/method/messages.send?v=5.131&random_id=0",data={'peer_ids': [peer_id], 'reply_to': reply,'message': message,'access_token':tok}).content.decode('utf-8'))

TOKEN = "f9be64a1e6f348476488b694a16ebc5626ef46df7550159447b8d5404b99689de512e41c6b883a50053ee"
vks = vk_api.VkApi(token=TOKEN)
vks._auth_token()
longpoll = VkBotLongPoll(vks, "201726057")
vk = vks.get_api()
for event in longpoll.listen():
    print(event)
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.message['text'].lower() in ['начать', 'старт', 'bot', 'бот', '/start']:
            user_id = event.message["from_id"]
            text = f'''
            Привет, {vk.users.get(user_ids = [user_id])[0]["first_name"]}!
            Я бот рабочей команды NAC. Могу подсказать тебе что-нибудь, или позвать кожаного.
            Ты можешь выполнить следующие команды:
            /start - начать работу с ботом
            /newyear <текст> - приму предложения по проведению новогоднего фестиваля
            /subscribe - подписаться на рассылку
            /unsubscribe - отписаться от рассылки
            /human - позвать сотрудника.
            '''
            send(text,TOKEN,event.message['peer_id'])
            if subscribe_need_start(user_id):
                text= '''
                Оп! Это звук уведомления нашей интереснейшей рассылки.
                Никакого спама: мы присылаем только самые важные новости и полезные посты.
                
                Хочешь подписаться?
                '''
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('Подписаться', color=VkKeyboardColor.PRIMARY)
                keyboard.add_line()  # Переход на вторую строку
                keyboard.add_button('Нет, спасибо.', color=VkKeyboardColor.NEGATIVE)
                vk.messages.send(
                    peer_id=event.message['peer_id'],
                    random_id=0,
                    keyboard=keyboard.get_keyboard(),
                    message=text
                )
                
    
        if event.message['text'].lower() in ['че там']:
            a = vk.users.get(user_ids = [event.message["from_id"]])
            firstname = a[0]["first_name"]
            send(f'Информация о боте.\nВаш ID: {event.message["from_id"]}\nID беседы: {event.message["peer_id"]}\nID сообщества бота: {event.group_id}',TOKEN,event.message['peer_id'])
            
        if event.message['text'].lower() in ['подписаться', 'подписаться на рассылку']:
            a = vk.users.get(user_ids = [event.message["from_id"]])
            firstname = a[0]["first_name"]
            send(f'Спасибо, {firstname}! Теперь ты будешь получать уведомления о важных событиях.\n\nЧтобы отписаться от рассылки, напиши команду "Отписаться от рассылки".',TOKEN,event.message['peer_id'])
            db.write(
                {
                    "user_id": event.message["from_id"],
                    "subscribe": True
                }
            )
        if event.message['text'].lower() in ['отписаться', 'отписаться от рассылки', 'нет, спасибо.']:
            a = vk.users.get(user_ids = [event.message["from_id"]])
            firstname = a[0]["first_name"]
            send(f'{firstname}, жаль что ты отказался (-лась) от рассылки. Ты не будешь получать уведомления о важных событиях.\n\nЕсли передумаешь, напиши команду "Подписаться на рассылку".',TOKEN,event.message['peer_id'])
            db.remove(
                {
                    "user_id": event.message["from_id"]
                }
            )
        if event.message['text'].lower() in ['/human', 'позови человека']:
            a = vk.users.get(user_ids = [event.message["from_id"]])
            firstname = a[0]["first_name"]
            print(a)
            lastname = a[0]["last_name"]
            system_peer = 2000000003
            send(f'Похоже, мне не удалось тебе помочь, {firstname}.\n\nЯ позвал человека. Пожалуйста, сообщи ему, почему я не смог помочь тебе и как меня улучшить. Спасибо"',TOKEN,event.message['peer_id'])
            send(f'Модераторы, нужна помощь человеку @id{event.message["from_id"]} ({firstname} {lastname}) (VK ID {event.message["from_id"]}), помогите ему в ЛС сообщества.',TOKEN,system_peer)
        if event.message["text"].startswith("/newyear"):
            a = vk.users.get(user_ids = [event.message["from_id"]])
            firstname = a[0]["first_name"]
            lastname = a[0]["last_name"]
            system_peer = 2000000003
            add_text = event.message["text"].split("/newyear", maxsplit=1)[1]
            send(f'{firstname}, спасибо за помощь! Ваша идея звучит очень круто. Самый лучшие предложения получат призы!',TOKEN,event.message['peer_id'])
            send(f'Модераторы, пришло новогоднее предложение от @id{event.message["from_id"]} ({firstname} {lastname}) (VK ID {event.message["from_id"]}).\n\n Вот его текст: {add_text}',TOKEN,system_peer)
            
        if event.message["text"].startswith("/saysubs") and event.message["from_id"] == 514957030:
            add_text = event.message["text"].split("/saysubs", maxsplit=1)[1]
            adr = db.findall()
            for a in adr:
                send(f'Общая рассылка!\n\n{add_text}',TOKEN,a)
        
        if event.message["text"].startswith("/python") and event.message["from_id"] == 514957030:
            add_text = event.message["text"].split("/python", maxsplit=1)[1]
            user_id = event.message['peer_id']
            a = exec(add_text)
            send(f'{a}', TOKEN, event.message['peer_id'])