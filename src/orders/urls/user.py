from django.urls import path

from orders.views.user import (
    UserOrderCreateView,
    UserOrderListAPIView,
    UserOrderRetrieveAPIView,
    PromoEligibilityCheck
)

app_name = 'user'

urlpatterns = [
    path('order/', UserOrderCreateView.as_view(), name="order_create"),
    path('orders/', UserOrderListAPIView.as_view(), name="order_list"),
    path('order/<int:pk>/', UserOrderRetrieveAPIView.as_view(), name="order_retrieve"),
    path('promo-check/', PromoEligibilityCheck.as_view(), name="promo_check"),

    
]
