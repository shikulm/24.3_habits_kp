import json
from datetime import datetime, timedelta

from django_celery_beat.models import PeriodicTask, \
    IntervalSchedule

# Создаем интервал для повтора
def get_schedule(*args, **kwargs):
    """Создание расписания для периодической блокировки пользователей, котороые давно не подключались"""
    schedule, created = IntervalSchedule.objects.get_or_create(
         every=30,
         period=IntervalSchedule.SECONDS,
     )

    # Создаем задачу для повторения
    PeriodicTask.objects.create(
         interval=schedule,
         name='block_users',
         task='courses.tasks.block_user',
         args=json.dumps(['arg1', 'arg2']),
         kwargs=json.dumps({
            'be_careful': True,
         }),
         expires=datetime.utcnow() + timedelta(seconds=30)
     )