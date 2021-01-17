from developerstodaytest.core.mixins import ViewsetSerializerMixin
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from .models import Post
from .serializers import CreatePostSerializer, UpdatePostSerializer, ViewPostSerializer


class PostsViewset(ViewsetSerializerMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    serializer_class = {
        CreatePostSerializer: ["create"],
        UpdatePostSerializer: ["update", "partial_update"],
        ViewPostSerializer: ["list", "retrieve", "destroy"],
    }

    def get_queryset(self):
        request: Request = self.get_serializer_context()["request"]
        return Post.objects.filter(user=request.user)
