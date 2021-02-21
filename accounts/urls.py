from django.urls import include, path
from rest_framework import routers

from .views import CustomTokenView, RegistrationViewSet, UserViewSet

v1_router = routers.DefaultRouter()
v1_router.register(r'auth/email', RegistrationViewSet)
v1_router.register(r'users', UserViewSet)


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/token/', CustomTokenView.as_view()),
]
