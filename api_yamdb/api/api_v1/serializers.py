import datetime

from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title, User


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')


class NotAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role')
        read_only_fields = ('role',)


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True)
    confirmation_code = serializers.CharField(
        required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_blank=False)
    username = serializers.CharField(allow_blank=False)

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        """
        Check that usermane is not 'me' and it is new user or not.
        """
        if data['username'] == 'me':
            raise serializers.ValidationError(
                "Нельзя создать пользователя с именем 'me'"
            )
        user_by_username = User.objects.filter(
            username=data['username']).first()
        user_by_email = User.objects.filter(
            email=data['email']).first()

        if user_by_username != user_by_email and (
            user_by_username is not None or user_by_email is not None
        ):
            raise serializers.ValidationError(
                'Пользователь с таким именем или'
                ' адресом почты уже существует!'
            )
        return data

    def create(self, validated_data):
        user = User(**validated_data)
        user.confirmation_code = default_token_generator.make_token(user)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.confirmation_code = default_token_generator.make_token(
            instance
        )
        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        if request.method != 'PATCH' and Review.objects.filter(
            author=request.user,
            title=request.parser_context['kwargs']['title_id']
        ).exists():
            raise serializers.ValidationError(
                'Невозможно оставить больше одного отзыва на произведение!')
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    review = serializers.SlugRelatedField(
        slug_field='id',
        read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date', 'review')
        model = Comment


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'category',
            'genre',
            'description',
            'rating',
        )


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'category', 'genre', 'description',)

    def validate_year(self, value):
        now_year = datetime.datetime.now().year
        if value < 0 or value > now_year:
            raise serializers.ValidationError(
                f'Не верный год [ 0 .. {now_year} ]'
            )
        return value
