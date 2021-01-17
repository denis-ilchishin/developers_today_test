from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, verbose_name=_("post's title")
    )
    date_created = models.DateTimeField(default=now, verbose_name=_("date of creation"))
    date_modified = models.DateTimeField(
        verbose_name=_("date of modification"), null=True
    )

    @property
    def uri(self):
        return reverse("posts:post-detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")
        ordering = ("-date_created",)
        get_latest_by = ("-date_created",)
