from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

from .views import PostViewSet, GroupViewSet, CommentViewSet, FollowViewSet

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('groups', GroupViewSet)
router.register('follow', FollowViewSet, basename='follow')
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/jwt/create/', TokenObtainPairView.as_view(), name='jwt-create'),
    path('v1/jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('v1/jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify'),
]
