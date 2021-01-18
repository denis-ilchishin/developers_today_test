from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Post


class PostTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="newuser")
        self.post = Post.objects.create(
            title="Some already existing post", author=self.user
        )

    def test_create_post(self):
        post_data = {"title": "Some new post"}

        self.client.force_authenticate(self.user)
        response = self.client.post(reverse("v1:posts:post-list"), post_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        self.assertIn("Location", response)

    def test_list_post(self):

        self.client.force_authenticate(self.user)
        response = self.client.get(reverse("v1:posts:post-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_post(self):
        post_data = {"title": "Some new post title"}

        self.client.force_authenticate(self.user)
        response = self.client.put(
            reverse("v1:posts:post-detail", kwargs={"pk": self.post.pk}), post_data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.get(pk=self.post.pk).title, post_data["title"])

    def test_view_post(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(
            reverse("v1:posts:post-detail", kwargs={"pk": self.post.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_post(self):
        self.client.force_authenticate(self.user)
        response = self.client.delete(
            reverse("v1:posts:post-detail", kwargs={"pk": self.post.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)
