from django.urls import path
from authentication.views import UserRegistrationAPIView, UserLoginAPIView, UserTokenAPIView, UserPasswordChange

app_name = 'authentication'

urlpatterns = [
    path('users/', UserRegistrationAPIView.as_view(), name="list"),
    path('login/', UserLoginAPIView.as_view(), name="login"),
    path('tokens/<key>/', UserTokenAPIView.as_view(), name="token"),
    path('password_change/', UserPasswordChange.as_view(), name="password_change"),
]
