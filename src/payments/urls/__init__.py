from django.urls import path, include

app_name = 'payments'

urlpatterns = [
    path('user/', include('payments.urls.user'), name='user.api'),
]
