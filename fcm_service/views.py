from django.shortcuts import get_object_or_404

from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from fcm_service.models import FCMToken
from fcm_service.serializers import FCMTokenSerializer, FCMTokenUpdateSerializer, PushMessagesSerializer

from composeexample.permissions import OwnerEditOnly


class FCMTokenCreateAPIView(CreateAPIView, ListAPIView):
    queryset = FCMToken.objects.all()
    permission_classes = []
    serializer_class = FCMTokenSerializer

    # edited to bring the current user fcm token
    def list(self, request, *args, **kwargs):
        obj = get_object_or_404(self.queryset, user=request.user)
        serializer = self.serializer_class(obj)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class FCMTokenUpdateAPIView(UpdateAPIView):
    queryset = FCMToken.objects.all()
    permission_classes = [OwnerEditOnly]
    serializer_class = FCMTokenUpdateSerializer


class PushMessagesListApiView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PushMessagesSerializer

    def list(self, request, *args, **kwargs):
        self.queryset = request.user.push_messages.all().order_by("-created_at")
        return super(PushMessagesListApiView, self).list(request, *args, **kwargs)
