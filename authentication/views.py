from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveDestroyAPIView
from authentication.serializers import UserRegistrationSerializer, UserLoginSerializer, TokenSerializer


class UserRegistrationAPIView(CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = serializer.instance
        token, created = Token.objects.get_or_create(user=user)
        data = serializer.data
        data["token"] = token.key

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class UserLoginAPIView(GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                data=TokenSerializer(token).data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserTokenAPIView(RetrieveDestroyAPIView):
    lookup_field = "key"
    serializer_class = TokenSerializer
    queryset = Token.objects.all()

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user)

    def retrieve(self, request, key, *args, **kwargs):
        if key == "current":
            instance = Token.objects.get(key=request.auth.key)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return super(UserTokenAPIView, self).retrieve(request, key, *args, **kwargs)

    def destroy(self, request, key, *args, **kwargs):
        if key == "current":
            Token.objects.get(key=request.auth.key).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super(UserTokenAPIView, self).destroy(request, key, *args, **kwargs)


# @login_required
# @require_http_methods(["POST"])
# def update_password(request):
#     """update the user password given the old and the new passwords"""
#     current_password = request.POST.get('currentPassword', '')
#     new_password = request.POST.get('newPassword', '')
#     new_password_confirmation = request.POST.get('confirmNewPassword', '')
#     user = authenticate(username=request.user.username, password=current_password)
#
#     if user is not None:
#         if new_password == new_password_confirmation:
#             request.user.set_password(new_password)
#             request.user.save()
#             message = "Password has been reset."
#             status = True
#         else:
#             message = "new password and new password confirmation differ."
#             status = False
#     else:
#         message = "old password is not right, please try again."
#         status = False
#
#     response = JsonResponse({
#         "answer": {
#             "message": message,
#             "status": status
#         },
#     })
#     return response
