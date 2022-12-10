from django.urls import path, include

app_name = 'orders'

urlpatterns = [
    path('admin/', include('orders.urls.admin'), name='admin.api'),
    path('user/', include('orders.urls.user'), name='user.api'),
]
