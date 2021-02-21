from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models

from .validators import validate_score

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Category's name")
    slug = models.SlugField(
        unique=True,
        max_length=200,
        default="slug",
        verbose_name="Category's URL"
    )

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name="Genre's name")
    slug = models.SlugField(
        unique=True,
        max_length=200,
        default="slug",
        verbose_name="Genre's URL"
    )

    class Meta:
        verbose_name = "genre"
        verbose_name_plural = "genres"
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        null=True,
        default="",
        verbose_name="Title's name"
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        related_name="titles",
        null=True,
        verbose_name="Title's category"
    )
    genre = models.ManyToManyField(
        Genre,
        related_name="titles",
        verbose_name="Title's genre(s)"
    )
    year = models.IntegerField(
        db_index=True,
        validators=[
            RegexValidator(
                regex=r"\d\d\d\d",
                message='Year must be 4 digits',
                code='invalid_year'
            )
        ]
    )
    description = models.TextField(
        verbose_name="Title's description"
    )

    class Meta:
        verbose_name = "title"
        verbose_name_plural = "titles"
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Review(models.Model):
    title_id = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews",
        verbose_name="Review's name"
    )
    text = models.TextField(verbose_name="Review's text")
    score = models.IntegerField(
        default=5, verbose_name="Review's score", validators=[validate_score])
    pub_date = models.DateTimeField(
        "Publication date", auto_now_add=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Review's author"
    )

    class Meta:
        verbose_name = "review"
        verbose_name_plural = "reviews"
        ordering = ["-pub_date"]

    def __str__(self):
        return f'{self.author} wrote {self.text}, score: {self.score}'


class Comment(models.Model):
    """
    Это комментарий к отзыву (ревью) о фильме.
    Фильм -> Отзыв к фильму -> Комментарий к отзыву
    """
    title_id = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="comments",
        verbose_name="Comment's title ID"
    )
    review_id = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments",
        verbose_name="Comment's review ID"
    )
    text = models.TextField(
        verbose_name="Comment's text"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Comment's author"
    )
    pub_date = models.DateTimeField("Publication date", auto_now_add=True)

    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"
        ordering = ["-pub_date"]

    def __str__(self):
        return f'{self.author} wrote {self.text}'
