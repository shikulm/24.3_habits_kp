from django.core.management import BaseCommand
from services import add_course


class Command(BaseCommand):
    """ Создает новый курс в БД. Выполняется из командной строки
    Параметры:
     - Навзание курса (обязательный позиционный параметр)
     - Описание курса (именованный аргумент - d или --description)
     ***Пример использования***
        > python -m manage.py add_course 'Базы данных' -d 'Изучаются основы реляционных БД b SQL'
    """

    help = u'Добавление курса'

    def add_arguments(self, parser):
        """Добавление аргументов в класс"""
        parser.add_argument('title', type=str, help='Название курса', )
        parser.add_argument('-d', '--description', type=str, help='Описание курса', )

    def handle(self, *args, **options):
        """Обработка вызова команды"""
        title = options['title']
        description = options['description']
        if description:
            add_course(title=title, description=description)
        else:
            add_course(title=title)
