import django_filters
from .models import Payment


class PaymentFilter(django_filters.FilterSet):
    """
    Фильтры для платежей
    """
    course = django_filters.NumberFilter(field_name='paid_course', lookup_expr='exact')
    lesson = django_filters.NumberFilter(field_name='paid_lesson', lookup_expr='exact')

    payment_method = django_filters.ChoiceFilter(choices=Payment.PAYMENT_METHOD_CHOICES)

    payment_date_from = django_filters.DateTimeFilter(field_name='payment_date', lookup_expr='gte')
    payment_date_to = django_filters.DateTimeFilter(field_name='payment_date', lookup_expr='lte')

    ordering = django_filters.OrderingFilter(
        fields=(
            ('payment_date', 'payment_date'),
            ('amount', 'amount'),
        ),
        field_labels={
            'payment_date': 'Дата оплаты',
            'amount': 'Сумма оплаты',
        }
    )

    class Meta:
        model = Payment
        fields = ['course', 'lesson', 'payment_method']
