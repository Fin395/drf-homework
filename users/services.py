import stripe

from config.settings import API_STRIPE_KEY


stripe.api_key = API_STRIPE_KEY


def create_stripe_product(product_name):
    """Создаем продукт в stripe."""

    product = stripe.Product.create(name=product_name)
    return product


def create_stripe_price(amount, product):
    """Создаем цену в stripe."""

    price = stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product_data={"name": f"Курс {product.get("name")}"},
    )
    return price


def create_stripe_session(price):
    """Создаем в stripe сессию для получения ссылки на оплату."""

    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )

    return session.get("id"), session.get("url")
