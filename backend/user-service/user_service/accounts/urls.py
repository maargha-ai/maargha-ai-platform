from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import RegisterView
from .views import LogoutView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", TokenObtainPairView.as_view()),
    path("logout/", LogoutView.as_view()),

]
