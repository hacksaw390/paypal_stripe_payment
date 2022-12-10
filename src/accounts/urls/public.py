from django.urls import path


from accounts.views.public import (
    login,
    refreshed_token,
    logout,
    UserRegisterView,
    RequestPasswordResetEmail,
    PasswordTokenCheckAPI,
    SetNewPasswordAPIView,
    get_user_data_from_google,
    get_user_data_from_facebook,
)

app_name = 'public'

urlpatterns = [
     path('login/', login, name='user_login_api'),
     path('refresh-token/', refreshed_token, name='user_token_refresh_api'),
     path('register/', UserRegisterView.as_view(), name='register'),
     path('logout/', logout, name='user_logout'),

     # Reset Password
     path('reset/', RequestPasswordResetEmail.as_view(), name='reset'),
     path('password-reset/<uidb64>/<token>/',
          PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
     path('password-reset-complete/', SetNewPasswordAPIView.as_view(),
          name='password-reset-complete'),

     # Social Auth
     path('google-auth/', get_user_data_from_google, name = 'get_user_data_from_google'),
     path('fb-auth/', get_user_data_from_facebook, name = 'get_user_data_from_facebook')

]
