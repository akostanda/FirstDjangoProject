from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import User
from .serializers import UserRegistrationSerializer, UserLoginSerializer

class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = serializer.instance
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'message': 'You are successfully registered.',
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'token': token.key
        }, status=status.HTTP_201_CREATED)


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
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response({"error": "Invalid activation link"}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Email successfully verified!"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)


# class EventCreateAPIView(generics.CreateAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def perform_create(self, serializer):
#         serializer.save(organizer=self.request.user)
#
#
# class EventListAPIView(generics.ListAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     permission_classes = [permissions.AllowAny]
#
#
# class EventDetailAPIView(generics.RetrieveAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     permission_classes = [permissions.AllowAny]
#
#
# class EventUpdateAPIView(generics.UpdateAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def perform_update(self, serializer):
#         if self.get_object().organizer != self.request.user:
#             raise PermissionDenied("You can not make changes in this event, you are not the organizer.")
#         serializer.save()
#
#
# class EventDeleteView(generics.DestroyAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def perform_destroy(self, instance):
#         if instance.organizer != self.request.user:
#             raise PermissionDenied("You can not delete this event, you are not the organizer.")
#         instance.delete()
