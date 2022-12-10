import django_filters
from django.contrib.auth import get_user_model
from accounts.models import UserAddress
User = get_user_model()


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ('is_active',)


class UserAddressFilter(django_filters.FilterSet):
    class Meta:
        model = UserAddress
        fields = ('address_type',)