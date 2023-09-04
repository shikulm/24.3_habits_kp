from django.db import models

from users.models import NOT_NULLABLE, NULLABLE, User


# Create your models here.

class Course(models.Model):
    """Хранит данные по курсам"""
    title = models.CharField(max_length=150, verbose_name='название', **NOT_NULLABLE, help_text="Название курса")
    preview = models.ImageField(upload_to='course/', verbose_name='превью', **NULLABLE, help_text="Превью курса")
    description = models.TextField(verbose_name='описание', **NULLABLE, help_text="Описание курса")

    def __str__(self):
        """Выводит наименование курса при выводе на печать модели"""
        return f"{self.title}"

    class Meta:
        verbose_name ='курс'
        verbose_name_plural ='курсы'
        ordering = ('title',)


class Lesson(models.Model):
    """Хранит данные по урокам. Содержит внешний ключ на модель с курсами (Course)"""
    title = models.CharField(max_length=150, verbose_name='название', **NOT_NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)
    preview = models.ImageField(upload_to='course/', verbose_name='превью', **NULLABLE)
    video_url = models.CharField(max_length=200, verbose_name='ссылка на видео', **NULLABLE)
    course = models.ForeignKey(to=Course, verbose_name='курс', related_name='lessons', on_delete=models.CASCADE, **NULLABLE)


    def __str__(self):
        """
        Выводит наименование урока при выводе на печать модели
        :return: строка с названием курса
        """
        return f"{self.title}"

    class Meta:
        verbose_name ='урок'
        verbose_name_plural ='уроки'
        ordering = ('title',)

class Payment(models.Model):
    """Хранит данные по оплате курса или урока.
    Содержит внешние ключи на модели с курсами (Course), уроками (Lesson) (заполняются в зависимости от того, за что проводится оплата)
        и внешний ключ к модели с пользователями (User)
    """
    CASH = 'cash'
    NON_CASH = 'non-cash'

    PAYMENT_METHOD = ((CASH, "наличные"), (NON_CASH, "перевод на счет"))

    user = models.ForeignKey(to=User, verbose_name='пользователь', related_name='payments', **NOT_NULLABLE, on_delete=models.CASCADE,
                             help_text="Пользователь, оплативший обучение")
    date_pay = models.DateField(auto_now_add=True, verbose_name='дата оплаты', **NOT_NULLABLE, help_text="Дата оплаты")
    course = models.ForeignKey(to=Course, verbose_name='курс', related_name='payments', **NULLABLE, on_delete=models.CASCADE, help_text="Оплачиваемый курс")
    lesson = models.ForeignKey(to=Lesson, verbose_name='урок', related_name='payments', **NULLABLE, on_delete=models.CASCADE, help_text="Оплачиваемый урок")
    payment_amount = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='сумма оплаты', **NOT_NULLABLE, help_text="Сумма оплаты")
    payment_method = models.CharField(max_length=150, choices=PAYMENT_METHOD, verbose_name='способ оплаты', default=NON_CASH,
                                      help_text="Способ оплаты. Варианты значений: ('cash'/'non-cash'), т.е. ('наличные'/'перевод на счет')")

    def __str__(self):
        """Выводит информацию по оплате при печати"""
        if self.course:
            return f"{self.user} оплатил курс {self.course} {self.date_pay} на сумму {self.payment_amount} ({self.payment_method})"
        else:
            return f"{self.user} оплатил урок {self.lesson} {self.date_pay} на сумму {self.payment_amount} ({self.payment_method})"

    class Meta:
        verbose_name ='оплата'
        verbose_name_plural ='оплата'
        ordering = ('-date_pay',)



