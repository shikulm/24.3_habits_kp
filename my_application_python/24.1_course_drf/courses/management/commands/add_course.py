from django.core.management import BaseCommand
from services import add_course


class Command(BaseCommand):

    help = u'Добавление курса'

    def add_arguments(self, parser):
        # Почта
        parser.add_argument('title', type=str, help='Название курса', )
        parser.add_argument('-d', '--description', type=str, help='Описание курса', )

    def handle(self, *args, **options):
        title = options['title']
        description = options['description']
        if description:
            add_course(title=title, description=description)
        else:
            add_course(title=title)
