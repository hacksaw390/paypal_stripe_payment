import django_filters
from orders.models import Order


class AdminOrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = ('order_status',)