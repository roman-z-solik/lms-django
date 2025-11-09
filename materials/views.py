from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from django.urls import reverse
from .models import Course, Lesson, Payment
from .serializers import (
    CourseSerializer,
    LessonSerializer,
    PaymentSerializer,
    PaymentCreateSerializer,
)
from .services.stripe_service import stripe_service


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для CRUD операций с курсами.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]


class LessonListView(generics.ListAPIView):
    """
    Generic-класс для получения списка уроков.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]


class LessonRetrieveView(generics.RetrieveAPIView):
    """
    Generic-класс для получения одного урока.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]


class LessonCreateView(generics.CreateAPIView):
    """
    Generic-класс для создания урока.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]


class LessonUpdateView(generics.UpdateAPIView):
    """
    Generic-класс для изменения урока.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]


class LessonDestroyView(generics.DestroyAPIView):
    """
    Generic-класс для удаления урока.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.AllowAny]


# class PaymentCreateView(generics.CreateAPIView):
#     """
#     Создание платежа для курса
#     """
#
#     queryset = Payment.objects.all()
#     serializer_class = PaymentCreateSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         course_id = serializer.validated_data["course_id"]
#         user = request.user
#
#         try:
#             course = Course.objects.get(id=course_id)
#         except Course.DoesNotExist:
#             return Response(
#                 {"error": "Курс не найден"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#         existing_payment = Payment.objects.filter(
#             user=user,
#             course=course,
#             status__in=[Payment.Status.PENDING, Payment.Status.PROCESSING],
#         ).first()
#
#         if existing_payment:
#             return Response(
#                 {"detail": "Активный платеж для этого курса уже существует"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#
#         try:
#             product = stripe_service.create_product(
#                 name=course.title, description=course.description
#             )
#
#             price = stripe_service.create_price(
#                 product_id=product.id, amount=course.price
#             )
#
#             success_url = request.build_absolute_uri(
#                 reverse("payment-success", kwargs={"pk": "CHECKOUT_SESSION_ID"})
#             )
#             cancel_url = request.build_absolute_uri(reverse("payment-cancel"))
#
#             success_url = success_url.replace(
#                 "CHECKOUT_SESSION_ID", "{CHECKOUT_SESSION_ID}"
#             )
#
#             session = stripe_service.create_checkout_session(
#                 price_id=price.id, success_url=success_url, cancel_url=cancel_url
#             )
#
#             payment = Payment.objects.create(
#                 user=user,
#                 course=course,
#                 amount=course.price,
#                 stripe_product_id=product.id,
#                 stripe_price_id=price.id,
#                 stripe_session_id=session.id,
#                 payment_url=session.url,
#                 status=Payment.Status.PENDING,
#             )
#
#             response_serializer = PaymentSerializer(payment)
#             return Response(response_serializer.data, status=status.HTTP_201_CREATED)
#
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
                    {"error": "Курс не найден"},
                    status=status.HTTP_400_BAD_REQUEST
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
