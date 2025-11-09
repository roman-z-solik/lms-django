import stripe
from django.conf import settings
from django.utils.translation import gettext_lazy as _

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeService:
    """Сервис для работы с Stripe API"""

    @staticmethod
    def create_product(name, description=None):
        """Создание продукта в Stripe"""
        try:
            product = stripe.Product.create(name=name, description=description)
            return product
        except stripe.error.StripeError as e:
            raise Exception(_(f"Ошибка создания продукта в Stripe: {str(e)}"))

    @staticmethod
    def create_price(product_id, amount, currency="rub"):
        """Создание цены в Stripe"""
        try:
            amount_in_cents = int(amount * 100)

            price = stripe.Price.create(
                product=product_id,
                unit_amount=amount_in_cents,
                currency=currency,
            )
            return price
        except stripe.error.StripeError as e:
            raise Exception(_(f"Ошибка создания цены в Stripe: {str(e)}"))

    @staticmethod
    def create_checkout_session(price_id, success_url, cancel_url):
        """Создание сессии для оплаты"""
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price": price_id,
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=success_url,
                cancel_url=cancel_url,
            )
            return session
        except stripe.error.StripeError as e:
            raise Exception(_(f"Ошибка создания сессии оплаты в Stripe: {str(e)}"))

    @staticmethod
    def get_session_status(session_id):
        """Получение статуса сессии оплаты"""
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            return session
        except stripe.error.StripeError as e:
            raise Exception(_(f"Ошибка получения статуса сессии: {str(e)}"))
