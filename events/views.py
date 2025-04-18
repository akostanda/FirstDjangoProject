from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status, permissions

from .models import Event
from .filters import EventFilter
from FirstDjangoProject import settings
from .serializers import EventSerializer


class EventCreateAPIView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response({
            'message': 'Event successfully created!',
            'event': serializer.data
        }, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)


class EventListAPIView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter


class EventDetailAPIView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]


class EventUpdateAPIView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        if self.get_object().organizer != self.request.user:
            raise PermissionDenied("You cannot make changes in this event, you are not the organizer.")
        serializer.save()


class EventDeleteAPIView(generics.DestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.organizer != self.request.user:
            raise PermissionDenied("You cannot delete this event, you are not the organizer.")
        instance.delete()


class EventAddParticipantAPIView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        event = self.get_object()
        user = request.user

        if  user == event.organizer:
            return Response({
                "message": "The organizer cannot be added as a participant."
            }, status=400)

        if user in event.participant.all():
            return Response({
                "message": "You are already a participant of this event."
            }, status=400)

        event.participant.add(user)
        self.send_notification_email(user)

        return Response({
            "message": "You have been successfully added as a participant.",
            "event": self.get_serializer(event).data
        })

    def send_notification_email(self, user):
        send_mail(
            subject="You are successfully registered",
            message=f"Hi {user.username}, thank you for joining our event!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
