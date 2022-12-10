from django.urls import path

from accounts.views.user import (
    user_password_change,
    UserProfileRetrieveUpdateAPIView,
    UserAddressListCreateAPIView,
    UserAddressRetrieveUpdateAPIView
)

app_name = 'user'

urlpatterns = [
    path('password-change/', user_password_change, name='user_password_change'),
    path('profile/', UserProfileRetrieveUpdateAPIView.as_view(),
        name='user_profile_view_update'),
    path('address/', UserAddressListCreateAPIView.as_view(),
        name='user_address_list_create'),
    
    path('address/<int:pk>/', UserAddressRetrieveUpdateAPIView.as_view(),
        name='user_address_retrieve_update'),
]
