from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("post's title"))
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, verbose_name=_("post's author")
    )
    date_created = models.DateTimeField(default=now, verbose_name=_("date of creation"))
    date_modified = models.DateTimeField(
        verbose_name=_("date of modification"), null=True
    )

    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")
        ordering = ("-date_created",)
        get_latest_by = ("-date_created",)


class PostComment(models.Model):
    post = models.ForeignKey(
        "Post",
        on_delete=models.CASCADE,
        related_name="comments",
        related_query_name="post",
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name=_("post comment author"),
    )
    content = models.CharField(max_length=250, verbose_name=_("post comment text"))
    date_created = models.DateTimeField(default=now, verbose_name=_("date of creation"))
    date_modified = models.DateTimeField(
        verbose_name=_("date of modification"), null=True
    )

    class Meta:
        verbose_name = _("post comment")
        verbose_name_plural = _("post comments")
        ordering = ("-date_created",)
        get_latest_by = ("-date_created",)
