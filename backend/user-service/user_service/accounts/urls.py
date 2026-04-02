from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import LogoutView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", TokenObtainPairView.as_view()),
    path("logout/", LogoutView.as_view()),
]
