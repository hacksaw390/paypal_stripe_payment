from django.urls import path

from payments.views.user import (
    stripe_webhook,
    Status
    )

app_name = 'user'

urlpatterns = [
    path('webhook/', stripe_webhook),
    path('status/', Status.as_view()),
    
]
