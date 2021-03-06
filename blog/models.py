import datetime

from django.db import models
from django.db.models import (SlugField,
                              CharField,
                              TextField,
                              DateTimeField,
                              URLField,
                              ForeignKey)
from django.utils import timezone
from electronicheart.users.models import User


class Entry(models.Model):

    title = CharField(max_length=250)
    subtitle = CharField(max_length=250)
    slug = SlugField(max_length=250, default='slug')
    content = TextField(default="")
    publishing_date = DateTimeField(default=timezone.now)
    creation_date = DateTimeField(default=timezone.now)
    next = URLField(null=True, blank=True)
    previous = URLField(null=True, blank=True)
    # tags = TaggableManager()

    class Meta:
        abstract = True


class Tutorial(Entry):

    type = 'tutorial'
    author = ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='tutorials')
    # thumbnail = FilerImageField(related_name="tutorial_thumbnail" on_delete=models.CASCADE, null=True)

