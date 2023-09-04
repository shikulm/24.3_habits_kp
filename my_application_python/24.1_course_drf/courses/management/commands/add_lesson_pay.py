from django.core.management import BaseCommand
from services import AddLessonPayment


class Command(BaseCommand):
    """ Создает запись по новой оплате урока в БД (т-ца Payment). Выполняется из командной строки терминала
    Параметры:
     - Код урока (обязательный позиционный параметр lesson_id)
     - Сумма оплаты (обязательный позиционный параметр payment_amount)
     - Код пользователя (именованный аргумент -u или --user_id). По умолчанию пользователь с кодом 1.
     - Способ оплаты (именованный аргумент -m или --payment_method).
            Допустимы значения: 'cash' (наличные) и 'non-cash' (перевод на счет) По умолчанию cash.
     В поле date_pay будет занесена текущая дата, в поле cource_id - Null
     ***Важно:***
     Если указан код урока, который отсутствует в БД, будет вызываться исключение
     ***Пример использования***
        > python -m manage.py add_lesson_pay 1 3500.00 -u 2 -m 'non-cash'
    """
    help = u'Добавление оплаты урока'

    def add_arguments(self, parser):
        """Добавление аргументов в класс"""
        parser.add_argument('lesson_id', type=int, help='Код урока', )
        parser.add_argument('payment_amount', type=float, help='Сумма оплаты', )
        parser.add_argument('-u', '--user_id', type=int, help='Код пользователя', )
        parser.add_argument('-m', '--payment_method', type=int, help='Способ оплаты', )

    def handle(self, *args, **options):
        """Обработка вызова команды"""
        data_save = {
            'lesson_id': options['lesson_id'],
            'payment_amount': options['payment_amount'],
        }
        if options['user_id']:
            data_save['user_id'] = options['user_id']
        if options['payment_method']:
            data_save['payment_method'] = options['payment_method']

        course_payment_new = AddLessonPayment(**data_save)
        course_payment_new.create_and_save()

