from django.utils.timezone import now
from rest_framework import serializers

from .models import Post


class PostSerializerMeta:
    model = Post
    extra_kwargs = {
        "url": {
            "view_name": "posts:post-detail",
        },
    }


class CreatePostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=Post._meta.get_field("title").max_length)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta(PostSerializerMeta):
        fields = ("title", "user", "url")


class UpdatePostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=Post._meta.get_field("title").max_length)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    date_modified = serializers.HiddenField(default=now)

    class Meta(PostSerializerMeta):
        fields = ("title", "user", "date_modified")


class ViewPostSerializer(serializers.ModelSerializer):

    author = serializers.CharField(source="user.username")

    class Meta(PostSerializerMeta):
        fields = ("title", "author", "date_created", "date_modified", "url")
