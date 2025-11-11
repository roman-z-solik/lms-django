from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from django.urls import reverse
from .models import Course, Lesson, Payment, Subscription
from .serializers import (
    CourseSerializer,
    LessonSerializer,
    PaymentSerializer,
    PaymentCreateSerializer,
    SubscriptionSerializer
)
from .services.stripe_service import stripe_service
from users.permissions import IsOwner, IsOwnerOrModerator, IsNotModerator


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для CRUD операций с курсами.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        """
        Разграничение прав доступа для курсов:
        - Создание: авторизованные пользователи (не модераторы)
        - Удаление: владелец или администратор
        - Просмотр и редактирование: владелец, модератор или администратор
        """
        if self.action == "create":
            permission_classes = [permissions.IsAuthenticated, IsNotModerator]
        elif self.action == "destroy":
            permission_classes = [permissions.IsAuthenticated, IsOwner | permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated, IsOwnerOrModerator | permissions.IsAdminUser]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Автоматически привязываем курс к текущему пользователю"""
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Фильтрация queryset:
        - Модераторы и администраторы видят все курсы
        - Обычные пользователи видят только свои курсы
        """
        queryset = super().get_queryset()
        user = self.request.user

        if not user.is_authenticated:
            return Course.objects.none()

        if user.is_staff or user.groups.filter(name="moderators").exists():
            return queryset

        return queryset.filter(owner=user)


class LessonListView(generics.ListAPIView):
    """
    Generic-класс для получения списка уроков.
    """

    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrModerator | permissions.IsAdminUser]

    def get_queryset(self):
        """
        Фильтрация уроков:
        - Модераторы и администраторы видят все уроки
        - Обычные пользователи видят только свои уроки
        """
        user = self.request.user

        if user.is_staff or user.groups.filter(name="moderators").exists():
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=user)


class LessonRetrieveView(generics.RetrieveAPIView):
    """
    Generic-класс для получения одного урока.
    """

    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrModerator | permissions.IsAdminUser]

    def get_queryset(self):
        """
        Фильтрация уроков:
        - Модераторы и администраторы видят все уроки
        - Обычные пользователи видят только свои уроки
        """
        user = self.request.user

        if user.is_staff or user.groups.filter(name="moderators").exists():
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=user)


class LessonCreateView(generics.CreateAPIView):
    """
    Generic-класс для создания урока.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsNotModerator]

    def perform_create(self, serializer):
        """Автоматически привязываем урок к текущему пользователю"""
        serializer.save(owner=self.request.user)


class LessonUpdateView(generics.UpdateAPIView):
    """
    Generic-класс для изменения урока.
    """

    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrModerator | permissions.IsAdminUser]

    def get_queryset(self):
        """
        Фильтрация уроков:
        - Модераторы и администраторы могут редактировать все уроки
        - Обычные пользователи могут редактировать только свои уроки
        """
        user = self.request.user

        if user.is_staff or user.groups.filter(name="moderators").exists():
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=user)


class LessonDestroyView(generics.DestroyAPIView):
    """
    Generic-класс для удаления урока.
    """

    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner | permissions.IsAdminUser]

    def get_queryset(self):
        """
        Фильтрация уроков:
        - Администраторы могут удалять все уроки
        - Обычные пользователи могут удалять только свои уроки
        """
        user = self.request.user

        if user.is_staff:
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=user)


class PaymentCreateView(generics.CreateAPIView):
    """
    Создание платежа для курса
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            print("=== Payment Create Started ===")
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            course_id = serializer.validated_data["course_id"]
            user = request.user

            # Получаем объект курса из базы данных
            try:
                course = Course.objects.get(id=course_id)
                print(f"Course: {course.title}, Price: {course.price}")
            except Course.DoesNotExist:
                return Response(
                    {"error": "Курс не найден"}, status=status.HTTP_400_BAD_REQUEST
                )

            existing_payment = Payment.objects.filter(
                user=user,
                course=course,
                status__in=[Payment.Status.PENDING, Payment.Status.PROCESSING],
            ).first()

            if existing_payment:
                return Response(
                    {"detail": "Активный платеж для этого курса уже существует"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            print("Creating Stripe objects...")
            product = stripe_service.create_product(
                name=course.title, description=course.description
            )

            price = stripe_service.create_price(
                product_id=product.id, amount=course.price
            )

            success_url = request.build_absolute_uri(
                reverse("payment-success", kwargs={"pk": "CHECKOUT_SESSION_ID"})
            )
            cancel_url = request.build_absolute_uri(reverse("payment-cancel"))

            success_url = success_url.replace(
                "CHECKOUT_SESSION_ID", "{CHECKOUT_SESSION_ID}"
            )

            session = stripe_service.create_checkout_session(
                price_id=price.id, success_url=success_url, cancel_url=cancel_url
            )

            payment = Payment.objects.create(
                user=user,
                course=course,
                amount=course.price,
                stripe_product_id=product.id,
                stripe_price_id=price.id,
                stripe_session_id=session.id,
                payment_url=session.url,
                status=Payment.Status.PENDING,
            )

            response_serializer = PaymentSerializer(payment)
            print("=== Payment Create Success ===")
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"=== ERROR: {str(e)} ===")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PaymentStatusView(generics.RetrieveAPIView):
    """
    Проверка статуса платежа
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        payment = self.get_object()

        try:
            session = stripe_service.get_session_status(payment.stripe_session_id)

            if session.payment_status == "paid":
                payment.status = Payment.Status.SUCCEEDED
            elif session.payment_status == "unpaid":
                payment.status = Payment.Status.FAILED
            payment.save()

            serializer = self.get_serializer(payment)
            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"error": f"Ошибка при проверке статуса: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PaymentSuccessView(generics.RetrieveAPIView):
    """
    Страница успешной оплаты (для редиректа из Stripe)
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        session_id = self.kwargs.get("pk")
        return Payment.objects.get(stripe_session_id=session_id, user=self.request.user)


class PaymentCancelView(generics.GenericAPIView):
    """
    Страница отмены оплаты (для редиректа из Stripe)
    """

    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response(
            {"detail": "Оплата была отменена. Вы можете попробовать снова."},
            status=status.HTTP_200_OK,
        )


class SubscriptionCreateView(generics.CreateAPIView):
    """
    Создание подписки на курс
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SubscriptionDestroyView(generics.DestroyAPIView):
    """
    Удаление подписки на курс
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class SubscriptionListView(generics.ListAPIView):
    """
    Список подписок пользователя
    """
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user, is_active=True)
      