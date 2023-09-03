from django.core.management import BaseCommand
from services import add_lesson


class Command(BaseCommand):

    help = u'Добавление урока'

    def add_arguments(self, parser):
        # Почта
        parser.add_argument('course_id', type=int, help='Код курса', )
        parser.add_argument('title', type=str, help='Название курса', )
        parser.add_argument('-d', '--description', type=str, help='Описание курса', )

    def handle(self, *args, **options):
        course_id = options['course_id']
        title = options['title']
        description = options['description']
        if description:
            add_lesson(course_id=course_id, title=title, description=description)
        else:
            add_lesson(course_id=course_id, title=title)