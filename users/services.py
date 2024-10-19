import stripe
import os
from dotenv import load_dotenv
from forex_python.converter import CurrencyRates, CurrencyCodes

load_dotenv()

stripe.api_key = os.getenv("STRIPE_API_KEY")



def convert_rub_to_usd(amount):
    """ пока не реализовываем, т.к. он глючит. Ошибка с JSON (forex-python)
        по дефолту ставим курс 100
        Конвертируем в base_cur (руб)  в dest_cur (доллары)
    """

    # c = CurrencyRates()
    # name_usd = codes.get_currency_name('USD')
    # codes = CurrencyCodes()
    rate_ = 100
    return int(amount) / int(rate_)


def create_product_stripe(course):
    """ Создаем продукт
        response:
        {
          "id": "prod_NWjs8kKbJWmuuc",
          "object": "product",
          "active": true,
          "created": 1678833149,
          "default_price": null,
          "description": null,
          "images": [],
          "marketing_features": [],
          "livemode": false,
          "metadata": {},
          "name": "Gold Plan",
          "package_dimensions": null,
          "shippable": null,
          "statement_descriptor": null,
          "tax_code": null,
          "unit_label": null,
          "updated": 1678833149,
          "url": null
        }
     """

    print('create_product_stripe course: ', course.name)
    return stripe.Product.create(name=course.name)


def create_price_stripe(product, price):
    print('create_price_stripe product: ', product, 'price: ', price)
    return stripe.Price.create(
        product=product.id,
        currency="usd",
        unit_amount=int(price * 100),
    )


def create_stripe_session(price):
    """ Создаем сессию в stripe"""

    session = stripe.checkout.Session.create(
        # success_url - куда мы перенаправим пользователя после успешной оплаты.
        success_url="http://127.0.0.1:8000/users/",
        # указываем id нашего продукта и количество.
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    # возвращаем url и id
    return session.get("id"), session.get("url")


if __name__ == '__main__':
    """ тестируем конверсию """
    rate = convert_rub_to_usd(120000)
    print(rate)
