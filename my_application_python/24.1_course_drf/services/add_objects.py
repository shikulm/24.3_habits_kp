import select
import sys
from random import random, randint, choice

from courses.models import Course, Lesson, Payment
from users.models import User


def add_course(title: str, description: str= None):
    """Создает новую запись по курсу"""
    return Course.objects.create(title = title, description = description)


def add_lesson(course_id: int, title: str, description: str = None):
    """Создает новую запись по уроку"""
    # try:
    course = Course.objects.filter(pk=course_id)
    if course.exists():
        #  Курс верный
        # course = Course.objects.get(pk=course_id)
        lesson = Lesson.objects.create(title=title, description=description, course=course[0])
        return lesson
    else:
        # Передан несуществующий код курса
        raise ValueError(f"Курса с кодом {course_id} не существует")


class AddPayment:
    """Класс для создания оплаты курса или урока"""
    COURSE = 'cource'
    LESSON = 'lesson'
    TYPE_OBJECT = (COURSE, LESSON)

    @property
    def user(self):
        """Возвращает объект польззователя"""
        return self._user

    @user.setter
    def user(self, user_id: int):
        """Создает объект пользователя по его id"""
        try:
            self._user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            # Передан несуществующий код пользователя
            sys.stdout.write(f"Пользователь с кодом {user_id} не существует")
    #
    @property
    def course(self):
        """Возвращает объект курса"""
        return self._course

    @course.setter
    def course(self, course_id: int):
        """Создает объект курса по его id"""
        try:
            self._course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            # Передан несуществующий код курса
            sys.stdout.write(f"Курс с кодом {course_id} не существует")

    @property
    def lesson(self):
        """Возвращает объект урока"""
        return self._lesson

    @lesson.setter
    def lesson(self, lesson_id: int):
        """Создает объект урока по его id"""
        try:
            self._lesson = Lesson.objects.get(pk=lesson_id)
        except Lesson.DoesNotExist:
            # Передан несуществующий код курса
            sys.stdout.write(f"Урок с кодом {lesson_id} не существует")

    @property
    def type_payment_object(self):
        """Возвращает тип объекта"""
        return self._type_payment_object

    @type_payment_object.setter
    def type_payment_object(self, type_object: str):
        """Создает свойство с типом оплачиваемого объекта (курс или урок)"""
        if type_object in self.TYPE_OBJECT:
            self._type_payment_object = type_object
        else:
            raise ValueError(f"Тип объекта {type_object} неправильный. Укажите один из вариантов: {self.TYPE_OBJECT}")
            # sys.stdout.write(f"Тип объекта {type_object} неправильный. Укажите один из вариантов: {self.TYPE_OBJECT}")

    @property
    def data_payment(self):
        """Возвращает объект урока"""
        self._data_payment = {"user": self.user,
                              "payment_amount": self.payment_amount,
                              "payment_method": self.payment_method}
        if self.type_payment_object == self.COURSE:
            self._data_payment['course'] = self.course
        else:
            self._data_payment['lesson'] = self.lesson

        return self._data_payment


    def __init__(self, payment_object_id: int, type_payment_object: str = COURSE, user_id: int = 1, payment_amount: float = 0.0, payment_method: str = None):
        self.user = user_id
        self.payment_amount = payment_amount
        self.payment_method = Payment.CASH if not payment_method else payment_method
        self.type_payment_object = type_payment_object
        if type_payment_object == self.COURSE:
            # Сохраняем переданный курс
            self.course = payment_object_id
        else:
            self.lesson = payment_object_id


    def create_and_save(self):
        # print(self.data_payment)
        return Payment.objects.create(**self.data_payment)



class AddCoursePayment(AddPayment):
    """Класс для создания оплаты курса"""
    def __init__(self, course_id: int, user_id: int = 1, payment_amount: float = 0.0, payment_method: str = None):
        super().__init__(payment_object_id=course_id, type_payment_object = self.COURSE, user_id= user_id,
                         payment_amount = payment_amount, payment_method= payment_method)


class AddLessonPayment(AddPayment):
    def __init__(self, lesson_id: int, user_id: int = 1, payment_amount: float = 0.0, payment_method: str = None):
        super().__init__(payment_object_id=lesson_id, type_payment_object = self.LESSON, user_id= user_id,
                         payment_amount = payment_amount, payment_method= payment_method)


def fill_courses():
    """ Заполнение БД группой записей"""
    # Количество курсов
    max_courses = 5
    max_lessons = 5
    max_payment = 10
    min_payment_amount = 1000
    max_payment_amount = 150000


    cnt_courses = randint(1, max_courses)
    ind_course = Course.objects.all().count()
    for id_c in range(cnt_courses+1):
        # Заполняем курсы
        ind_course+=1
        course_mew = add_course(title=f"Курс № {ind_course}", description=f"Описание курса № {ind_course}")
        # Заполняем уроки курса
        cnt_lessons = randint(1, max_lessons)
        for id_l in range(cnt_lessons+1):
            lesson_mew = add_lesson(course_id=course_mew.pk, title=f"Урок № {ind_course}.{id_l+1}", description=f"Описание урока № {ind_course}.{id_l+1} из курса № {ind_course}")
            # Заполняем оплату за курсы/уроки
            cnt_payment = randint(1, max_payment)
            for id_p in range(cnt_payment + 1):
                # Случайно определяем будет ли оплата за урок или курс
                type_parent = choice([1, 2])
                # Случайно подбираем сумму оплаты
                payment_amount = randint(min_payment_amount, max_payment_amount)
                # Случайно подбираем способ оплаты
                payment_method = choice(list(Payment.PAYMENT_METHOD))[0]
                # Создаем запись по оплате
                if type_parent == 1:
                    #  Оплата за курс
                    payment_mew = AddCoursePayment(course_id=course_mew.pk, payment_amount=payment_amount, payment_method = payment_method)
                else:
                    #  Оплата за урок
                    payment_mew = AddLessonPayment(lesson_id=lesson_mew.pk, payment_amount=payment_amount, payment_method = payment_method)
                payment_mew.create_and_save()











