from django.urls import path

from .views import (
    EventCreateAPIView,
    EventListAPIView,
    EventDetailAPIView,
    EventUpdateAPIView,
    EventDeleteAPIView,
    EventAddParticipantAPIView,
)

urlpatterns = [
    path('create/', EventCreateAPIView.as_view(), name='event-creat'),
    path('', EventListAPIView.as_view(), name='event-list'),
    path('<int:pk>/', EventDetailAPIView.as_view(), name='event-detail'),
    path('<int:pk>/update/', EventUpdateAPIView.as_view(), name='event-update'),
    path('<int:pk>/delete/', EventDeleteAPIView.as_view(), name='event-delete'),
    path('<int:event_id>/add_participant/', EventAddParticipantAPIView.as_view(), name='event-add-participant'),

]

