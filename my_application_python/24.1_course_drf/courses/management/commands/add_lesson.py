from django.core.management import BaseCommand
from services import add_lesson


class Command(BaseCommand):
    """ Создает запись по новому уроку в БД. Выполняется из командной строки
    Параметры:
     - Код курса (обязательный позиционный параметр course_id)
     - Навзание урока (обязательный позиционный параметр title)
     - Описание урока (именованный аргумент - d или --description)
     Остальные поля в таблице (preview и video_url) заполняются Null
     ***Важно:***
     Если указан код курса, который отсутствует в БД, будет вызываться исключение
     ***Пример использования***
        > python -m manage.py add_lesson 1 'Введение в базы данных' -d 'Описываются основные поля БД'
    """


    help = u'Добавление урока'

    def add_arguments(self, parser):
        """Добавление аргументов в класс"""
        parser.add_argument('course_id', type=int, help='Код курса', )
        parser.add_argument('title', type=str, help='Название курса', )
        parser.add_argument('-d', '--description', type=str, help='Описание курса', )

    def handle(self, *args, **options):
        """Обработка вызова команды"""
        course_id = options['course_id']
        title = options['title']
        description = options['description']
        if description:
            add_lesson(course_id=course_id, title=title, description=description)
        else:
            add_lesson(course_id=course_id, title=title)