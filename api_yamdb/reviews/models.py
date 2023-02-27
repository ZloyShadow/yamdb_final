import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    ROLE_CHOICES = [
        (USER, USER),
        (ADMIN, ADMIN),
        (MODERATOR, MODERATOR),
    ]

    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
        blank=False,
        null=False
    )
    role = models.CharField(
        'Role',
        max_length=255,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True
    )
    bio = models.TextField(
        'biography',
        blank=True,
    )
    first_name = models.CharField(
        'name',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'surname',
        max_length=150,
        blank=True
    )
    confirmation_code = models.CharField(
        'confirmation code',
        max_length=255,
        null=True,
        blank=False
    )

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        verbose_name = 'User'
        ordering = ('id',)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(
        "Категория произведения",
        max_length=200,
        unique=True,
        help_text="Введите категорию произведения.",
    )
    slug = models.SlugField(
        "URL",
        unique=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        "Название жанра",
        max_length=200,
        unique=True,
        help_text="Введите название жанра",
    )
    slug = models.SlugField(
        "URL",
        unique=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Genre"

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=256, verbose_name='Название фильма'
    )
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(datetime.date.today().year)],
        verbose_name='Год выпуска', db_index=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        blank=True, null=True, related_name='category_title',
        verbose_name='Категория'
    )
    description = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        default=None,
        through='GenreTitle',
        related_name='genre',
        verbose_name='Жанр',
        blank=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Title"

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name="Произведение"
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name="Жанр"
    )

    class Meta:
        verbose_name = "Произведение и жанр"
        verbose_name_plural = "Произведения и жанры"

    def __str__(self):
        return f"{self.title}, жанр - {self.genre}"


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )
    score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Review'
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"],
                name='author_title',
            ),
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Comment'
        default_related_name = 'comments'
