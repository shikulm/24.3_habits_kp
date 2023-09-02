from django.db import models

from users.models import NOT_NULLABLE, NULLABLE


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




