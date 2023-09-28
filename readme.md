<h2> Перед выполнением проекта выполните команды </h2>

<h3> в Ubuntu: </h3>

>sudo service postgresql start

>sudo service redis-server start 

<h3> В терминале выполняем команды для начала работы </h3>

Установка библиотек:
> python -m pip install -r requirement.txt

Активация среды окружения (для Linux):
> source env/bin/activate 

Запуск сервера:
>  python manage.py runserver

<h3> В процессе работы могут потребоваться команды </h3>

Фиксация изменений в git
>git commit -a -m ' '

Запуск отложенных задач celery (с декоратором @shared_task)
>celery -A config worker -l INFO 
 
Запуск периодических задач celery (с декоратором @shared_task)
> celery -A config beat -l INFO -S django --logfile=celery.log

или
> celery -A config beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler