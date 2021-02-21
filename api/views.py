from accounts.permissions import AdminOrOwnerOrReadOnly, AdminOrReadOnly
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.filters import SearchFilter

from .filters import TitleFilter
from .models import Category, Comment, Genre, Review, Title
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          TitleSerializerGet)
from .viewsets import ListCreateDestroyViewSet


class TitlesViewSet(viewsets.ModelViewSet):
    """
    С помощью аннотации мы добавляем поле с рейтингом
    к каждому объекту модели (средняя оценка)
    """
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('-id')

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, AdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = TitleFilter
    filterset_fields = ['name']

    def get_serializer_class(self):
        """
        При разных типах запросов нам нужно представлять
        данные в разном виде, для этого определяем для
        метода GET отдельный класс сериалайзера, унаследованный
        от основного
        """
        if self.request.method == 'GET':
            return TitleSerializerGet
        else:
            return TitleSerializer


class CategoriesViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, AdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name', 'slug']
    search_fields = ['name']
    lookup_field = 'slug'


class GenresViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, AdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['name', 'slug']
    search_fields = ['name']
    lookup_field = 'slug'


class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, AdminOrOwnerOrReadOnly]

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        serializer.save(
            title_id=self.get_title(),
            author=self.request.user,
        )

    def get_queryset(self):
        """
        Возвращаем только отзывы к конкретному тайтлу
        """
        return self.get_title().reviews.all()


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, AdminOrOwnerOrReadOnly]

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_review(self):
        return get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title_id=self.get_title()
        )

    def perform_create(self, serializer):
        serializer.save(
            title_id=self.get_title(),
            review_id=self.get_review(),
            author=self.request.user
        )

    def get_queryset(self):
        """
        Возвращаем комментарии к конкретному отзыву
        """
        return self.get_review().comments.all()
