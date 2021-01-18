from django.urls import path
from django.urls.conf import include
from rest_framework.routers import SimpleRouter

from . import views

app_name = "posts"

router = SimpleRouter()
router.register("post", views.PostsViewset, "post")

urlpatterns = [path("", include(router.urls))]
