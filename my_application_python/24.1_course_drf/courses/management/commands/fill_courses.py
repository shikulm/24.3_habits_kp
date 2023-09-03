from django.core.management import BaseCommand
from services import fill_courses


class Command(BaseCommand):

    help = u'Заполняет базу данных с курсами случайными значениями'

    def handle(self, *args, **options):
        fill_courses()

