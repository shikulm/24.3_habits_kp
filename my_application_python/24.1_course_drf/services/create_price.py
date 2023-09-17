import stripe
from django.shortcuts import get_object_or_404

from conf.settings import STRIPE_API_KEY
from courses.models import Course, Payment


# stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"
# stripe.api_key = "sk_test_51NqDBYJxrEpVE1z5rgKoeKvnGqDW9krXwCVeFkJgwsFbh6LmbLkLibGNNdMHy1V7i1B67yMUPAWEKbu6vjCi134L007nW9woTT"
# stripe.api_key = STRIPE_API_KEY

# starter_subscription = stripe.Product.create(
#   name="Starter Subscription",
#   description="$12/Month subscription",
# )
#
# starter_subscription_price = stripe.Price.create(
#   unit_amount=1200,
#   currency="usd",
#   recurring={"interval": "month"},
#   product=starter_subscription['id'],
# )
#
# # Save these identifiers
# print(f"Success! Here is your starter subscription product id: {starter_subscription.id}")
# print(f"Success! Here is your starter subscription price id: {starter_subscription_price.id}")

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
  """Проверка и обновление стауса оплаты и обновление """
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

# Отслеживание платежей
# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
# import stripe
# stripe.api_key = "sk_test_51NqDBYJxrEpVE1z5rgKoeKvnGqDW9krXwCVeFkJgwsFbh6LmbLkLibGNNdMHy1V7i1B67yMUPAWEKbu6vjCi134L007nW9woTT"
#
# stripe.PaymentLink.create(
#   line_items=[{"price": '{{PRICE_ID}}', "quantity": 1}],
#   after_completion={"type": "redirect", "redirect": {"url": "https://example.com"}},
# )
