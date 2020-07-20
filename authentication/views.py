from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import RetrieveDestroyAPIView, CreateAPIView, UpdateAPIView

from authentication.choices import TOKEN_TYPES_DICT
from authentication.serializers import UserRegistrationSerializer, UserLoginSerializer, TokenSerializer, \
    UserPasswordChangeSerializer, CustomTokenSerializer, ResetPasswordSerializer

from authentication.models import User, CustomToken


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
            token_data = TokenSerializer(token).data
            return Response(
                data=token_data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserPasswordChange(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserPasswordChangeSerializer

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            user.set_password(request.data["new_password"])
            user.save()
            token, created = Token.objects.get_or_create(user=serializer.object['user'])
            if created:
                token.save()

            return Response(
                data={'status': 'password set'},
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


class CustomTokenCreateAPIView(CreateAPIView):
    permission_classes = []
    serializer_class = CustomTokenSerializer

    def create(self, request, *args, **kwargs):
        username = self.request.data.get("username", None)
        user_obj = get_object_or_404(User, username=username)
        request.data._mutable = True
        request.data["user"] = user_obj.id
        request.data.pop("username")
        # 2 : "password reset" type
        request.data["_type"] = TOKEN_TYPES_DICT.get("password reset", 2)
        request.data._mutable = False

        response = super(CustomTokenCreateAPIView, self).create(request, *args, **kwargs)
        request_created = (response.status_code == 201)
        if request_created:
            return Response(
                data={
                    "info": "your request has been added, please check your email."
                }, status=status.HTTP_200_OK
            )
        else:
            return response


class CustomTokenRetrieveDestroyUpdateAPIView(RetrieveDestroyAPIView, UpdateAPIView):
    queryset = CustomToken.objects.filter(expired=False, destroyed=False)
    permission_classes = []
    serializer_class = CustomTokenSerializer

    def retrieve(self, request, *args, **kwargs):
        token_key = self.request.data.get("key", None)
        token_obj = get_object_or_404(self.queryset, key=token_key)
        instance = token_obj
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        token_key = self.request.data.get("key", None)
        token_obj = get_object_or_404(self.queryset, key=token_key)
        self.serializer_class = ResetPasswordSerializer
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = token_obj.user
            new_password = self.request.data.get("password", None)
            user.set_password(raw_password=new_password)
            user.save()
            token_obj.expired = True
            token_obj.save()

            return Response(
                data={'status': 'password set'},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
