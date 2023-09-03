from django.core.management import BaseCommand
from services import AddCoursePayment


class Command(BaseCommand):

    help = u'Добавление оплаты курса'

    def add_arguments(self, parser):
        parser.add_argument('course_id', type=int, help='Код курса', )
        parser.add_argument('payment_amount', type=float, help='Сумма оплаты', )
        parser.add_argument('-u', '--user_id', type=int, help='Код пользователя', )
        parser.add_argument('-m', '--payment_method', type=int, help='Способ оплаты', )

    def handle(self, *args, **options):
        data_save = {
            'course_id': options['course_id'],
            'payment_amount': options['payment_amount'],
        }
        if options['user_id']:
            data_save['user_id'] = options['user_id']
        if options['payment_method']:
            data_save['payment_method'] = options['payment_method']

        course_payment_new = AddCoursePayment(**data_save)
        course_payment_new.create_and_save()

