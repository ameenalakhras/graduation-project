from django.urls import path
from authentication.views import UserRegistrationAPIView, UserLoginAPIView, UserTokenAPIView

app_name = 'authentication'

urlpatterns = [
    path('users/', UserRegistrationAPIView.as_view(), name="list"),
    path('users/login/', UserLoginAPIView.as_view(), name="login"),
    path('tokens/<key>/', UserTokenAPIView.as_view(), name="token"),
]