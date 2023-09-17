import stripe
from django.shortcuts import get_object_or_404

from conf.settings import STRIPE_API_KEY
from courses.models import Course, Payment



def create_price(id_cource: int):
  """Создание оплаты за курс. Параметр - код курса"""
  stripe.api_key = STRIPE_API_KEY
  # Ищем данные по оплачиваемому курсу
  course = get_object_or_404(Course, pk=id_cource)
  if course:
    # Создаем продукт для оплаты
    course_for_sell = stripe.Product.create(
      name=course.title,
      description=course.description,
    )

    # Создание оплаты
    starter_subscription_price = stripe.Price.create(
      unit_amount=course.price*100,
      currency="rub",
      recurring={"interval": "month"}, #mode = subscription
      product=course_for_sell['id'],
    )

    # Создание сессии для оплаты
    session = stripe.checkout.Session.create(
      success_url="https://example.com/success",
      line_items=[
        {
          "price": starter_subscription_price.id,
          "quantity": 1,
        },
      ],
      mode="subscription",
    )

    # # Создание ссылки для оплаты курса
    # payment_link = stripe.PaymentLink.create(line_items=[{"price": starter_subscription_price.id, "quantity": 1}])

    # print(f"Success! Here is your starter subscription product id: {course_for_sell.id}")
    # print(f"Success! Here is your starter subscription price id: {starter_subscription_price.id}")
    # return payment_link
    return session

def retrive_session(id_pay: int):
  """ Отслеживание платежей """
  stripe.api_key = STRIPE_API_KEY

  pay =  get_object_or_404(Payment, pk=id_pay)
  # Если оплата с таким кодом есть
  if pay:
    session_new = stripe.checkout.Session.retrieve(
      pay.session_id,
    )
    pay.payment_status = session_new.status
    pay.payment_link = session_new
    pay.save()
    return session_new

# create_price(1)


