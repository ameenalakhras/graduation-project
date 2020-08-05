from django.urls import path
from fcm_service.views import FCMTokenCreateAPIView, FCMTokenUpdateAPIView, PushMessagesListApiView

app_name = 'fcm_service'

urlpatterns = [
    path("fcm_token/", FCMTokenCreateAPIView.as_view(), name="fcm_token_create"),
    path("fcm_token/<int:pk>", FCMTokenUpdateAPIView.as_view(), name="fcm_token_update"),
    path("notifications/", PushMessagesListApiView.as_view(), name="push_notifications")
]
