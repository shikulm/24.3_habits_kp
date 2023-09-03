from django.db import models

from users.models import NOT_NULLABLE, NULLABLE, User


# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='название', **NOT_NULLABLE)
    preview = models.ImageField(upload_to='course/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name ='курс'
        verbose_name_plural ='курсы'
        ordering = ('title',)


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='название', **NOT_NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)
    preview = models.ImageField(upload_to='course/', verbose_name='превью', **NULLABLE)
    video_url = models.CharField(max_length=200, verbose_name='ссылка на видео', **NULLABLE)
    course = models.ForeignKey(to=Course, verbose_name='курс', related_name='lessons', on_delete=models.CASCADE, **NULLABLE)


    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name ='урок'
        verbose_name_plural ='уроки'
        ordering = ('title',)

class Payment(models.Model):

    CASH = 'cash'
    NON_CASH = 'non-cash'

    PAYMENT_METHOD = ((CASH, "наличные"), (NON_CASH, "перевод на счет"))

    user = models.ForeignKey(to=User, verbose_name='пользователь', related_name='payments', **NOT_NULLABLE, on_delete=models.CASCADE)
    date_pay = models.DateField(auto_now_add=True, verbose_name='дата оплаты', **NOT_NULLABLE)
    course = models.ForeignKey(to=Course, verbose_name='курс', related_name='payments', **NULLABLE, on_delete=models.CASCADE)
    lesson = models.ForeignKey(to=Lesson, verbose_name='урок', related_name='payments', **NULLABLE, on_delete=models.CASCADE)
    payment_amount = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='сумма оплаты', **NOT_NULLABLE)
    payment_method = models.CharField(max_length=150, choices=PAYMENT_METHOD, verbose_name='способ оплаты', default=NON_CASH)

    def __str__(self):
        if self.course:
            return f"{self.user} оплатил курс {self.course} {self.date_pay} на сумму {self.payment_amount} ({self.payment_method})"
        else:
            return f"{self.user} оплатил урок {self.lesson} {self.date_pay} на сумму {self.payment_amount} ({self.payment_method})"

    class Meta:
        verbose_name ='оплата'
        verbose_name_plural ='оплата'
        ordering = ('-date_pay',)



