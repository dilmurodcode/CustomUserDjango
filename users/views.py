from rest_framework import generics
from . import models
from . import serializers
from rest_framework.response import Response


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = serializers.RegisterSerializer
    queryset = models.CustomUser.objects.all()


class CodeVerifyAPIView(generics.CreateAPIView):
    serializer_class = serializers.CodeVerificationSerializer
    queryset = models.CustomUser.objects.all()


class LoginAPIView(generics.CreateAPIView):
    serializer_class = serializers.LoginSerializer
    queryset = models.CustomUser.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        tokens = user.tokens()
        return Response(
            data={
                "data": tokens
            }, status=200
        )