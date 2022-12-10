from django.urls import path


from orders.views.admin import (
    AdminOrderListAPIView,
    AdminOrderRetrieveUpdateAPIView,
    PromoCodeListCreateAPIView,
    PromoCodeRetrieveUpdateAPIView
)

app_name = 'admin'

urlpatterns = [
   path('orders/', AdminOrderListAPIView.as_view(), name="order_list"),
   path('order/<int:pk>/', AdminOrderRetrieveUpdateAPIView.as_view(), name="order_retrieve"),
   path('promo-code/', PromoCodeListCreateAPIView.as_view(), name="promo_code_list_create"),
   path('promo-code/<int:pk>/', PromoCodeRetrieveUpdateAPIView.as_view(), name="promo_code_retrieve_update"),


]
