from django.urls import path

from .views import UserRegistrationAPIView, UserLoginAPIView, UserEmailConfirmationAPIView


urlpatterns = [
    path('registration/', UserRegistrationAPIView.as_view(), name='registration'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('email-confirmation/<str:uidb64>/<str:token>/', UserEmailConfirmationAPIView.as_view(), name='email-confirmation'),
]
