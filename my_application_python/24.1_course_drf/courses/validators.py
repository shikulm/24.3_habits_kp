from rest_framework import serializers
class UrlValidate:
    """Валидатор для проверки на отсутствие в материалах ссылок на сторонние ресурсы, кроме youtube.com"""
    def __init__(self, field):
        """Сохраняем поле, для колторого выполняем провекру"""
        self.field = field

    def __call__(self, value):
        """Проверка валидаци на отсуствие ссылок на сторонние ресурсы"""
        fld_val = dict(value).get(self.field)
        print(fld_val)
        if fld_val!=None and 'youtube.com' not in fld_val.lower():
            raise serializers.ValidationError('Ссылка может быть только на youtube')

