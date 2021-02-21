from django_filters import rest_framework as filters

from .models import Title


class TitleFilter(filters.FilterSet):
    """
    Класс помогает нам фильтровать по URL объекта
    """
    genre = filters.CharFilter(field_name="genre__slug")
    category = filters.CharFilter(field_name="category__slug")
    year = filters.NumberFilter
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Title
        fields = ['genre', 'category', 'year', 'name']
