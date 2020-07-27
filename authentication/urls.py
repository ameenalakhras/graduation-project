from django.urls import path
from authentication.views import UserRegistrationAPIView, UserLoginAPIView, UserTokenAPIView, UserPasswordChange, \
    CustomTokenCreateAPIView, CustomTokenRetrieveDestroyUpdateAPIView, FCMTokenCreateAPIView, \
    FCMTokenUpdateAPIView, PushMessagesListApiView

app_name = 'authentication'

urlpatterns = [
    path('users/', UserRegistrationAPIView.as_view(), name="list"),
    path('login/', UserLoginAPIView.as_view(), name="login"),
    path('tokens/<key>/', UserTokenAPIView.as_view(), name="token"),
    path('password_change/', UserPasswordChange.as_view(), name="password_change"),
    path("forgot_password/", CustomTokenCreateAPIView.as_view(), name="forgot_password"),
    path("reset_password/", CustomTokenRetrieveDestroyUpdateAPIView.as_view(), name="reset_password"),
    path("fcm_token/", FCMTokenCreateAPIView.as_view(), name="fcm_token_create"),
    path("fcm_token/<int:pk>", FCMTokenUpdateAPIView.as_view(), name="fcm_token_update"),
    path("notifications/", PushMessagesListApiView.as_view(), name="push_notifications")
]
