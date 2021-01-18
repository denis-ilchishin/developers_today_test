from django.urls import path
from django.urls.conf import include
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from . import views

app_name = "posts"

router = SimpleRouter()
router.register("post", views.PostsViewset, "post")


posts_router = routers.NestedSimpleRouter(router, "post", lookup="post")
posts_router.register("comment", views.PostCommentsViewset, basename="comment")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(posts_router.urls)),
]
