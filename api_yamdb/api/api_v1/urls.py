from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (APIGetToken, APISignup, CategoryViewSet, CommentViewSet,
                    GenreViewSet, ReviewViewSet, TitleViewSet, UsersViewSet)

router = SimpleRouter()

router.register(
    r'users',
    UsersViewSet,
    basename='users'
)
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
auth_patterns = [
    path('token/', APIGetToken.as_view(), name='get_token'),
    path('signup/', APISignup.as_view(), name='signup'),
]
urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include(auth_patterns)),
]
