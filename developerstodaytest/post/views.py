from typing import Any

from developerstodaytest.core.mixins import ViewsetSerializerMixin
from django.db.models.query import QuerySet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from . import serializers
from .models import Post, PostComment, PostUpvote


class PostsViewset(ViewsetSerializerMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    serializer_class = {
        serializers.CreatePostSerializer: ["create"],
        serializers.UpdatePostSerializer: ["update", "partial_update"],
        serializers.ViewPostSerializer: ["list", "retrieve", "destroy"],
    }

    def get_queryset(self) -> QuerySet:
        """Limit queryset to only current user's posts"""
        return Post.objects.filter(author=self.request.user)

    @action(detail=True, methods=["post"])
    def upvote(self, request: Request, **kwargs):
        post: Post = self.get_object()
        upvote, created = PostUpvote.objects.get_or_create(post=post, user=request.user)
        if created:
            status_code = status.HTTP_201_CREATED
        else:
            status_code = status.HTTP_204_NO_CONTENT

        return Response(status=status_code)


class PostCommentsViewset(ViewsetSerializerMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    serializer_class = {
        serializers.CreatePostCommentSerializer: ["create"],
        serializers.UpdatePostCommentSerializer: ["update", "partial_update"],
        serializers.ViewPostCommentSerializer: ["list", "retrieve", "destroy"],
    }

    def initial(self, *args, **kwargs):
        self.post_instance: Post = get_object_or_404(
            Post.objects.all(), pk=self.kwargs.get("post_pk")
        )

        return super().initial(*args, **kwargs)

    def get_queryset(self) -> QuerySet:
        """Limit queryset to only current user's post comments"""

        return PostComment.objects.filter(
            author=self.request.user, post=self.post_instance
        )

    def get_serializer_context(self) -> dict[str, Any]:
        return {**super().get_serializer_context(), "post": self.post_instance}
