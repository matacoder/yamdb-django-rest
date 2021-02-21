from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Category, Comment, Genre, Review, Title

User = get_user_model()


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    rating = serializers.IntegerField(read_only=True)

    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'slug']
        model = Category
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'slug']
        model = Genre
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitleSerializerGet(TitleSerializer):
    """
    Для метода GET отдельный сериалайзер
    """
    category = CategorySerializer()
    genre = GenreSerializer(many=True, read_only=True)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    title_id = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        """
        Защищаеся от дублей и неправильных оценок
        """
        if self.context['request'].method == 'POST':
            if Review.objects.filter(
                    author=self.context['request'].user,
                    title_id=self.context['view'].kwargs.get('title_id'),
            ).exists():
                raise serializers.ValidationError(
                    'Double posting is not allowed'
                )

        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    title_id = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    review_id = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )

    class Meta:
        fields = '__all__'
        model = Comment
