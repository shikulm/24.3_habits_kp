import datetime

from celery import shared_task
import requests
# from django.contrib.sites import requests
from django.http import request
from django.utils import timezone
from rest_framework.exceptions import status

from config.settings import HTTP_TG_BOT
from habits.models import Habit, MailingLog
from users.models import User


def send_messsage(habit: Habit):
    """Отправка сообщения в телеграм"""
    url = f"{HTTP_TG_BOT}/sendMessage"
    chat_id = habit.user.chat_id
    print("habit = ", habit)
    print("chat_id = ", chat_id)
    msg = f"Вам надо {habit.action} в {habit.place} в {habit.time_habit}"
    response = {'ok': False, "result": f"сhat_id пользователя телеграм {habit.user.telegram} не найден", "error_code": status.HTTP_404_NOT_FOUND}
    if chat_id:
        # Если id чата пользователя в telegram нашли, то
        # Определяем, граничную дату предыдущей отправки сообщения в телеграм, после которой потребуется повторная отправка
        threshold_date = datetime.datetime.now() - timezone.timedelta(days=habit.frequency)
        if not MailingLog.objects.filter(datetime_mailing__gte=threshold_date, ok=True).exists():
            # отправляем сообщение
            data = {'chat_id': chat_id, 'text': msg}
            print("data = ", data)
            response = requests.get(url, data).json()
        else:
            return response
    print("response = ", response)
    save_log(habit, response)

    return response


def update_chat_id():
    """Сохраняет chat_id пользователей в БД"""
    # получаем из телеграм информацию об обновлениях, ( обновлениях есть имя пользователя telegram и chat_id)
    url = f"{HTTP_TG_BOT}/getUpdates"
    response = requests.get(url).json()
    if response.get("ok"):
        # Получение списка уникальных соответсвий имен пользователей telegram и их chat_id
        user_chats = set([(el.get("message").get("chat").get("username"), el.get("message").get("chat").get("id")) for el in response.get("result")])
        # print("user_chat = ", user_chat)
        for user_chat in user_chats:
            User.objects.filter(telegram__iregex=user_chat[0]).update(chat_id=user_chat[1])



def save_log(habit, response):
    """Сохраение резульатов отправик сообщения в журнале"""
    MailingLog.objects.create(habit_id=habit.pk, ok=response.get("ok"),
                              result=response.get("result") if response.get("result") else response.get("description"),
                              error_code=response.get("error_code") if response.get("error_code") else None)


@shared_task
def send_to_telegram():
    """Основная задача для отправки рассылок в телеграм"""
    # Сопоставляем имена пользователей в telegram с chat_id пользователя
    update_chat_id()
    # Получаем спсиок задач, для которых нужно провести рассылку
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    habits_for_send = Habit.objects.filter(time_habit__hour=hour, time_habit__minute=minute)
    for habit in habits_for_send:
        response = send_messsage(habit)

