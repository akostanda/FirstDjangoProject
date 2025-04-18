from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from FirstDjangoProject import settings
from .models import User
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserEmailConfirmationSerializer

class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = serializer.instance
        token, _ = Token.objects.get_or_create(user=user)

        self.send_confirmation_email(user)

        return Response({
            'message': 'You are successfully registered.',
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'token': token.key
        }, status=status.HTTP_201_CREATED)

    def send_confirmation_email(self, user):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        verify_url = f"{settings.BASE_URL}/{settings.EMAIL_CONFIRMATION_URL}/{uid}/{token}/"

        send_mail(
            subject="Confirmation Email",
            message=f"Hi {user.username}, click the link to confirm your email address: {verify_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )


class UserLoginAPIView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'message': 'You are successfully logged in.',
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'token': token.key
        }, status=status.HTTP_200_OK)


class UserEmailConfirmationAPIView(generics.GenericAPIView):
    serializer_class = UserEmailConfirmationSerializer

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response({"success": False, "message": "Invalid activation link"}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"success": True, "message": "Email successfully confirmed"}, status=status.HTTP_200_OK)
        else:
            return Response({"success": False, "message": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
