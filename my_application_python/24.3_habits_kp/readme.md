<h1>О проекте </h1>
В 2018 году Джеймс Клир написал книгу «Атомные привычки», которая посвящена приобретению новых полезных привычек и искоренению старых плохих привычек.
В рамках проекта реализуется бэкенд-часть SPA веб-приложения.
В книге хороший пример привычки описывается как конкретное действие, которое можно уложить в одно предложение:

>я буду [ДЕЙСТВИЕ] в [ВРЕМЯ] в [МЕСТО]

За каждую полезную привычку необходимо себя вознаграждать или сразу после делать приятную привычку. Но при этом привычка не должна расходовать на выполнение больше 2 минут. <br>
В программе:
 - реализованы функции CRUD для создания, просмотра и редактирования привычек пользователей.
 - отправляяются напоминания пользователю о повторении привычки в соответсвии с графиком
 - выполняются проверка валидации и правил досупа к данным.


<h2> Перед выполнением проекта выполните команды: </h2>

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

Запуск отложенных задач celery (с декоратором @shared_task)
>celery -A config worker -l INFO 
 
Запуск периодических задач celery (с декоратором @shared_task)
> celery -A config beat -l INFO -S django --logfile=celery.log

или
> celery -A config beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler 


<h3> В процессе работы могут потребоваться команды </h3>

Фиксация изменений в git
>git commit -a -m ' '

Проверка покрытия кода тестами
> coverage run --source='.' manage.py test
> 
> coverage report
