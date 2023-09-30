import datetime
from smtplib import SMTPException

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from conf.settings import get_env_value
from courses.models import Course, Subscription, MailingLog
from users.models import User


def send_email(course: Course, user: User):
    '''Отправка письма об изменении курса course пользователю user'''
    res = 0
    res_txt = 'OK'
    try:
        res = send_mail(
            subject = f"Обновление курса {course.title}",
            message = f"Курс {course.title} обновился {course.last_update}. \n {course.description}. "
                      f"\n Автор курса {course.owner}. \n Цена: {course.price}.",
            from_email = get_env_value('EMAIL_HOST_USER'),
            recipient_list=[user.email],
            fail_silently=False
        )
    except SMTPException as e:
        res_txt = e

    MailingLog.objects.create(user_id=user.pk, course_id=course.pk, last_update=course.last_update,
                              status=MailingLog.STATUS_OK if res else MailingLog.STATUS_FAIL,
                              answer=res_txt)


@shared_task
def send_mails():
    """Отправляем письма всем подписчикам измененных курсов"""

    # Получаем список курсов, которые обновлялись более 4 часов назад
    dt_now = datetime.datetime.now(datetime.timezone.utc)-datetime.timedelta(hours=4)
    # dt_now = datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(minutes=5)
    courses_list = Course.objects.filter(last_update__lte=dt_now)
    # print("courses_list = ", courses_list)
    # qs = qs_today | qs_tomorrow

    # Перебор курсов для отправки сообщения
    for course in courses_list:
        # print("course = ", course)
        # Перебираем список рассылки
        cource_pk= course.pk
        for user in User.objects.filter(subscription__course_id=cource_pk):
            # print("user = ", user)
            if not MailingLog.objects.filter(course_id=cource_pk, user_id=user.pk, last_update=course.last_update).exists():
                print(f"send about change course '{course}' to {user}")
                # Отправляем сообщение, если информация об изменении раньше не отправлялась пользователю
                send_email(course, user)


@shared_task
def block_user():
    """Блокирует пользователей, которые не заходили более более месяца"""
    # Крайняя дата полдключения для блокировки
    threshold_date = timezone.now().date() -datetime.timedelta(days=30)
    # last_dt_block =  timezone.now()-datetime.timedelta(days=3)
    print(f"Блокируем всех, кто подключался ва последний раз до {threshold_date}")
    # Получаем списка пользователей для блокировки
    # users_for_block = User.objects.filter(last_login__lte=threshold_date)
    inactive_users = User.objects.filter(last_login__lte=threshold_date, is_active=True).update(is_active=False)
    # users_for_block = User.objects.all()
    # print("Пользователи для блокировки", inactive_users)
    # # Блокируем пользователей
    # for user in inactive_users :
    #     print(f"Заблокирован пользователь {user}")
    #     # user.update(is_active=False)
    #     user.is_active = False
    #     user.save()



