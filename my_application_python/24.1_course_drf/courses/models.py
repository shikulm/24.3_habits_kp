from django.db import models

from users.models import NOT_NULLABLE, NULLABLE, User


# Create your models here.

class Course(models.Model):
    """Хранит данные по курсам"""
    title = models.CharField(max_length=150, verbose_name='название', **NOT_NULLABLE, help_text="Название курса")
    preview = models.ImageField(upload_to='course/', verbose_name='превью', **NULLABLE, help_text="Превью курса")
    description = models.TextField(verbose_name='описание', **NULLABLE, help_text="Описание курса")
    owner = models.ForeignKey(to=User, verbose_name='Автор', on_delete=models.CASCADE, related_name='courses', default=1)
    price = models.PositiveIntegerField(default=1500, **NULLABLE, verbose_name='цена')
    last_update = models.DateTimeField(auto_now=True, verbose_name='дата последнего обновления', **NULLABLE)

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
    owner = models.ForeignKey(to=User, verbose_name='Автор', on_delete=models.CASCADE, related_name='lessons', default=1)
    price = models.PositiveIntegerField(default=1500, **NULLABLE, verbose_name='цена')
    last_update = models.DateTimeField(auto_now=True, verbose_name='дата последнего обновления', **NULLABLE)


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
    session_id = models.CharField(max_length=150, verbose_name='ID сессии Stripe', **NULLABLE,
                                      help_text="ID сессии Stripe")
    payment_link = models.TextField(verbose_name='сессия для оплаты', **NULLABLE, help_text="сессия для оплаты")
    payment_url = models.TextField(verbose_name='url для оплаты', **NULLABLE, help_text="url для оплаты")
    payment_status = models.CharField(max_length=150, verbose_name='статус оплаты', **NULLABLE, default='unpaid', help_text="статус оплаты")

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


class Subscription(models.Model):
    """Класс с подписями пользователей на курс"""
    course = models.ForeignKey(to=Course, verbose_name='курс', related_name='subscription', on_delete=models.CASCADE, **NOT_NULLABLE, help_text="Курс подписки")
    user = models.ForeignKey(to=User, verbose_name='пользователь', related_name='subscription', **NOT_NULLABLE, on_delete=models.CASCADE, help_text="Подписанный пользователь")
    date_subscripe = models.DateField(auto_now_add=True, verbose_name='дата подписки', **NOT_NULLABLE, help_text="Дата подписки")
    def __str__(self):
        """Выводит информацию по подписям"""
        return f"Пользователь {self.user} подписан на курс {self.course}"

    class Meta:
        verbose_name ='подписка'
        verbose_name_plural ='подписки'
        ordering = ('-date_subscripe',)
        unique_together = ('course', 'user',)


class MailingLog(models.Model):
    """Журнал рассылки информации об изменениях в курсах"""
    STATUS_OK = 'ok'
    STATUS_FAIL = 'fail'
    STATUSES = ((STATUS_OK, 'Успешно'),(STATUS_FAIL, 'Ошибка'))

    datetime_mailing = models.DateTimeField(auto_now_add=True, verbose_name='дата и время рассылки', **NOT_NULLABLE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='покупатель', **NOT_NULLABLE, related_name='mailing_log')
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, verbose_name='курс', **NOT_NULLABLE, related_name='mailing_log')
    last_update = models.DateTimeField(verbose_name='дата обновления курса', **NULLABLE)
    status = models.CharField(max_length=150, verbose_name='статус', choices=STATUSES, default=STATUS_OK, **NOT_NULLABLE)
    answer = models.TextField(verbose_name='ответ почтового сервера', **NULLABLE)


    def __str__(self):
        return f'{self.datetime_mailing} {self.client} {self.setting} {self.status}'

    class Meta:
        verbose_name = 'Запись журнала рассылки'
        verbose_name_plural = 'Журнал рассылок'
        ordering = ['-datetime_mailing',]

