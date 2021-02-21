from django.contrib.auth import get_user_model
from rest_framework import filters, permissions, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase

from .permissions import IsAdministrator
from .serializers import (CustomJWTSerializer, RegistrationSerializer,
                          UserSerializer)
from .viewsets import CreateOnlyViewSet

User = get_user_model()


class RegistrationViewSet(CreateOnlyViewSet):

    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (permissions.AllowAny,)


class CustomTokenView(TokenViewBase):

    serializer_class = CustomJWTSerializer
    permission_classes = (permissions.AllowAny,)


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsAdministrator,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'put', 'patch'],
            permission_classes=(permissions.IsAuthenticated,), url_path='me')
    def self_user_info(self, request):
        '''
        Get or update information about yourself.
        '''
        user = request.user
        if request.method == 'GET':
            serializer = self.serializer_class(user)
            return Response(serializer.data)

        if request.data.get('role') and not user.is_admin:
            raise serializers.ValidationError(
                'Only administrator can change the role.')

        serializer = self.serializer_class(
            instance=user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
