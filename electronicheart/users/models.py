from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, TextField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from filer.fields.image import FilerImageField


class User(AbstractUser):
    """Default user for electronicheart."""

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)

    # -- Profile information
    # The user should have some profile information, which is being displayed for example if that user is the
    # author of a blog post

    # A profile picture, optimally showing the face of the author
    image = FilerImageField(related_name="user_image", on_delete=models.CASCADE, null=True)

    # A short description about the author
    bio = TextField(default='')

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
