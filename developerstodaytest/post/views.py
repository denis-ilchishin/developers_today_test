from typing import Any

from developerstodaytest.core.mixins import ViewsetSerializerMixin
from django.db.models.query import QuerySet
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from . import serializers
from .models import Post, PostComment


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


class PostCommentsViewset(ViewsetSerializerMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    serializer_class = {
        serializers.CreatePostCommentSerializer: ["create"],
        serializers.UpdatePostCommentSerializer: ["update", "partial_update"],
        serializers.ViewPostCommentSerializer: ["list", "retrieve", "destroy"],
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.post: Post = get_object_or_404(
            Post.objects.all(), pk=self.kwargs.get("post_pk")
        )

    def get_queryset(self) -> QuerySet:
        """Limit queryset to only current user's post comments"""

        return PostComment.objects.filter(author=self.request.user, post=self.post)

    def get_serializer_context(self) -> dict[str, Any]:
        return {**super().get_serializer_context(), "post": self.post}
