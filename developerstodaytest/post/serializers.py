from django.utils.timezone import now
from rest_framework import serializers

from .models import Post, PostComment


class PostSerializerMeta:
    model = Post
    extra_kwargs = {
        "url": {
            "view_name": "v1:posts:post-detail",
        },
    }


class CreatePostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=Post._meta.get_field("title").max_length)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta(PostSerializerMeta):
        fields = ("title", "author", "url")


class UpdatePostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=Post._meta.get_field("title").max_length)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    date_modified = serializers.HiddenField(default=now)

    class Meta(PostSerializerMeta):
        fields = ("title", "author", "date_modified")


class ViewPostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username")

    class Meta(PostSerializerMeta):
        fields = ("title", "author", "date_created", "date_modified", "url")


class PostCommentSerializerMeta:
    model = PostComment


class PostCommentPostDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context["post"]

    def __repr__(self):
        return "%s()" % self.__class__.__name__


class CreatePostCommentSerializer(serializers.ModelSerializer):
    content = serializers.CharField(
        max_length=PostComment._meta.get_field("content").max_length
    )
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    post = serializers.HiddenField(default=PostCommentPostDefault())

    class Meta(PostCommentSerializerMeta):
        fields = (
            "post",
            "content",
            "author",
        )


class UpdatePostCommentSerializer(serializers.ModelSerializer):
    content = serializers.CharField(
        max_length=PostComment._meta.get_field("content").max_length
    )
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    post = serializers.HiddenField(default=PostCommentPostDefault())
    date_modified = serializers.HiddenField(default=now)

    class Meta(PostCommentSerializerMeta):
        fields = ("content", "author", "post", "date_modified")


class ViewPostCommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username")

    class Meta(PostCommentSerializerMeta):
        fields = (
            "content",
            "author",
            "post",
            "date_created",
            "date_modified",
        )
