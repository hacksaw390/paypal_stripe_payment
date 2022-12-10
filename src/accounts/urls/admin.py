from django.urls import path


from accounts.views.admin import (
    AdminUserListCreateApiView,
    AdminProfileRetrieveUpdateAPIView,
    AdminUserRetrieveUpdateAPIView,
    AdminCustomerLisApiView,
    AdminCustomerRetrieveAPIView
)

app_name = 'admin'

urlpatterns = [
    path('profile/', AdminProfileRetrieveUpdateAPIView.as_view(),
        name='profile'),
    path('users/', AdminUserListCreateApiView.as_view(),
        name='user_list_create'),
    path('user/<int:pk>/', AdminUserRetrieveUpdateAPIView.as_view(),
        name='user_retrieve_update'),

    path('customers/', AdminCustomerLisApiView.as_view(),
        name='customer_list'),
    
    path('customer/<int:pk>/', AdminCustomerRetrieveAPIView.as_view(),
        name='customer_retrieve'),

]
