from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from posts.models import Post, Group, Comment, Follow
from .serializers import PostSerializer, GroupSerializer, CommentSerializer, FollowSerializer, FollowCreateSerializer
from .permissions import IsAuthorOrReadOnly
from .permissions import PublicReadOnly
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [PublicReadOnly, IsAuthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = None
    permission_classes = [AllowAny]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        serializer.save(author=self.request.user, post_id=post_id)

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAuthenticated(), IsAuthorOrReadOnly()]
        return [IsAuthenticatedOrReadOnly()]

class PostListView(APIView):
    def get(self, request):
        queryset = Post.objects.all()
        paginator = LimitOffsetPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = PostSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class FollowViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Follow.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer

    def get_queryset(self):
        queryset = Follow.objects.filter(user=self.request.user)
        if search := self.request.query_params.get('search'):
            queryset = queryset.filter(following__username__icontains=search)
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return FollowCreateSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        following = get_object_or_404(
            User,
            username=serializer.validated_data['following']
        )
        
        if Follow.objects.filter(user=request.user, following=following).exists():
            return Response(
                {"detail": "Вы уже подписаны на этого пользователя"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if request.user == following:
            return Response(
                {"detail": "Нельзя подписаться на себя"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        follow = Follow.objects.create(user=request.user, following=following)
        return Response(
            FollowSerializer(follow, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            return Response(
                {'detail': 'Вы не можете отменить чужую подписку'},
                status=status.HTTP_403_FORBIDDEN
            )
        instance.delete()
