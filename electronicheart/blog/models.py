import datetime

from django.db import models
from django.db.models import (SlugField,
                              CharField,
                              TextField,
                              DateTimeField,
                              URLField,
                              ForeignKey)
from django.utils import timezone


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
