import datetime

from celery import shared_task
import requests
# from django.contrib.sites import requests
from django.http import request
from rest_framework.exceptions import status

from config.settings import HTTP_TG_BOT
from habits.models import Habit
from users.models import User


def send_messsage(user: User, msg: str):
    """Отправка сообщения в телеграм"""
    url = f"{HTTP_TG_BOT}/sendMessage"
    chat_id = user.chat_id
    response = {'ok': False, "result": f"сhat_id пользователя телеграм {user.telegram} не найден", "error_code": status.HTTP_404_NOT_FOUND}
    if chat_id:
        # Если id чата пользователя в telegram нашли, то отправляем сообщение
        data = {'chat_id': chat_id, 'text': msg}
        print("data = ", data)
        response = requests.get(url, data).json()
    print(response)

    # MailingLog.objects.create(user_id=user.pk, course_id=course.pk, last_update=course.last_update,
    #                           status=MailingLog.STATUS_OK if res else MailingLog.STATUS_FAIL,
    #                           answer=res_txt)
    return response




def update_chat_id():
    """Сохраняет chat_id пользователей в БД"""
    # получаем из телеграм информацию об обновлениях, ( обновлениях есть имя пользователя telegram и chat_id)
    url = f"{HTTP_TG_BOT}/getUpdates"
    # print("url=", url)
    # request.get
    response = requests.get(url).json()
    # print("response = ", response)
    if response.get("ok"):
        # Получение списка уникальных соответсвий имен пользователей telegram и их chat_id
        # user_chat = [(el.get("username"), el.get("id") ) for el in response.get("result").get("message").get("chat")]
        user_chats = set([(el.get("message").get("chat").get("username"), el.get("message").get("chat").get("id")) for el in response.get("result")])
        # print("user_chat = ", user_chat)
        for user_chat in user_chats:
            user = User.objects.filter(telegram__iregex=user_chat[0]).first()
            if user:
                user.chat_id=user_chat[1]
                user.save()


@shared_task
def send_to_telegram():
    """Основная задача для отправки рассылок в телеграм"""
    # Сопоставляем имена пользователей в telegram с chat_id пользователя
    update_chat_id()
    # Получаем спсиок задач, для которых нужно провести рассылку
    hour = datetime.datetime.now().hour
    # print("hour = ", hour)
    minute = datetime.datetime.now().minute
    # print("minute = ", minute)
    habits_for_send = Habit.objects.filter(time_habit__hour=hour, time_habit__minute=minute)
    # habits_for_send = Habit.objects.all()
    # print("habits_for_send = ", habits_for_send)
    for habit in habits_for_send:
        msg = f"Вам надо {habit.action} в {habit.place} в {habit.time_habit}"
        send_messsage(habit.user, msg)
