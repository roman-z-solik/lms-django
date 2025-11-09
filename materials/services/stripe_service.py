import stripe
from django.conf import settings
import uuid


class MockStripeService:
    """Мок-сервис для тестирования без реального Stripe"""

    @staticmethod
    def create_product(name, description=None):
        """Создание мок-продукта"""
        print(f"🔧 Mock: Creating product: {name}")
        mock_product = type("Product", (), {})()
        mock_product.id = f"prod_mock_{uuid.uuid4().hex[:8]}"
        return mock_product

    @staticmethod
    def create_price(product_id, amount, currency="rub"):
        """Создание мок-цены"""
        print(f"🔧 Mock: Creating price for product {product_id}, amount: {amount}")
        mock_price = type("Price", (), {})()
        mock_price.id = f"price_mock_{uuid.uuid4().hex[:8]}"
        return mock_price

    @staticmethod
    def create_checkout_session(price_id, success_url, cancel_url):
        """Создание мок-сессии"""
        print(f"🔧 Mock: Creating checkout session for price {price_id}")
        session_id = f"cs_mock_{uuid.uuid4().hex[:8]}"
        mock_session = type("Session", (), {})()
        mock_session.id = session_id
        mock_session.url = f"http://127.0.0.1:8000/mock-payment/{session_id}/"
        mock_session.payment_status = "unpaid"
        return mock_session

    @staticmethod
    def get_session_status(session_id):
        """Получение мок-статуса"""
        print(f"🔧 Mock: Getting session status: {session_id}")
        mock_session = type("Session", (), {})()
        mock_session.payment_status = "paid"
        return mock_session


class RealStripeService:
    """Реальный сервис для работы с Stripe API"""

    def __init__(self):
        if not getattr(settings, "STRIPE_SECRET_KEY", None):
            raise Exception("STRIPE_SECRET_KEY не настроен")

        # Настройка Stripe
        stripe.api_key = settings.STRIPE_SECRET_KEY
        print("✅ Real Stripe Service initialized")

    def create_product(self, name, description=None):
        """Создание продукта в Stripe"""
        try:
            print(f"✅ Stripe: Creating product: {name}")

            product = stripe.Product.create(
                name=name, description=description or "No description provided"
            )
            print(f"✅ Product created: {product.id}")
            return product

        except Exception as e:
            error_msg = f"Stripe Error: {str(e)}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)

    def create_price(self, product_id, amount, currency="rub"):
        """Создание цены в Stripe"""
        try:
            print(
                f"✅ Stripe: Creating price for product {product_id}, amount: {amount}"
            )

            amount_in_cents = int(float(amount) * 100)
            print(f"Amount in cents: {amount_in_cents}")

            price = stripe.Price.create(
                product=product_id,
                unit_amount=amount_in_cents,
                currency=currency,
            )
            print(f"✅ Price created: {price.id}")
            return price

        except Exception as e:
            error_msg = f"Stripe Error: {str(e)}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)

    def create_checkout_session(self, price_id, success_url, cancel_url):
        """Создание сессии для оплаты"""
        try:
            print(f"✅ Stripe: Creating checkout session for price {price_id}")

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
            print(f"✅ Session created: {session.id}")
            print(f"✅ Payment URL: {session.url}")
            return session

        except Exception as e:
            error_msg = f"Stripe Error: {str(e)}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)

    def get_session_status(self, session_id):
        """Получение статуса сессии оплаты"""
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            return session
        except Exception as e:
            raise Exception(f"Ошибка получения статуса сессии: {str(e)}")


class StripeService:
    """Умный сервис для работы с платежами"""

    def __init__(self):
        self.service = None
        self._initialize_service()

    def _initialize_service(self):
        """Инициализация сервиса с автоматическим выбором"""
        try:
            self.service = RealStripeService()
            print("🚀 Testing Real Stripe API...")
            stripe.Balance.retrieve()  # Простой запрос для проверки
            print("✅ Stripe Service: Real Stripe API подключен и работает")
            return
        except Exception as e:
            print(f"⚠️  Real Stripe недоступен: {str(e)}")

        print("🔧 Stripe Service: Используется Mock Service")
        self.service = MockStripeService()

    def create_product(self, name, description=None):
        try:
            return self.service.create_product(name, description)
        except Exception:
            print("🔄 Переключаемся на Mock Service после ошибки")
            self.service = MockStripeService()
            return self.service.create_product(name, description)

    def create_price(self, product_id, amount, currency="rub"):
        try:
            return self.service.create_price(product_id, amount, currency)
        except Exception:
            print("🔄 Переключаемся на Mock Service после ошибки")
            self.service = MockStripeService()
            return self.service.create_price(product_id, amount, currency)

    def create_checkout_session(self, price_id, success_url, cancel_url):
        try:
            return self.service.create_checkout_session(
                price_id, success_url, cancel_url
            )
        except Exception:
            print("🔄 Переключаемся на Mock Service после ошибки")
            self.service = MockStripeService()
            return self.service.create_checkout_session(
                price_id, success_url, cancel_url
            )

    def get_session_status(self, session_id):
        return self.service.get_session_status(session_id)


stripe_service = StripeService()
