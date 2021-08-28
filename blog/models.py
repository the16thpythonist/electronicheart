from __future__ import annotations
import datetime
from typing import List

from django.db import models
from django.db.models import (SlugField,
                              CharField,
                              TextField,
                              DateTimeField,
                              URLField,
                              ForeignKey)
from django.utils import timezone
from django.utils.text import slugify
from filer.fields.image import FilerImageField

from electronicheart.users.models import User


# == ACTUAL MODEL CLASSES

class Entry(models.Model):

    title = CharField(max_length=250)
    subtitle = CharField(max_length=250, default='', blank=True)
    description = CharField(max_length=200, default='', blank=True)
    slug = SlugField(max_length=250, default='auto', unique=True)
    content = TextField(default='')
    publishing_date = DateTimeField(default=timezone.now)
    creation_date = DateTimeField(default=timezone.now)
    next = URLField(null=True, blank=True)
    previous = URLField(null=True, blank=True)
    # tags = TaggableManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        if self.slug == 'auto':
            self.slug = slugify(self.title)
        super(Entry, self).save(*args, **kwargs)

    @classmethod
    def get_most_recent(cls, n: int) -> List[Entry]:

        entries = cls.objects.order_by('-publishing_date').exclude(publishing_date__gte=timezone.now()).all()[0:n]

        return entries


class Tutorial(Entry):

    type = 'tutorial'
    author = ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='tutorials')
    thumbnail = FilerImageField(related_name="tutorial_thumbnail", on_delete=models.CASCADE, null=True)


class Project(Entry):

    type = 'project'
    author = ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='projects')
    thumbnail = FilerImageField(related_name='project_thumbnail', on_delete=models.CASCADE, null=True)


# == UTILITY FUNCTIONS

def get_most_recent_entries(n: int,
                            entry_subclasses: List[type] = [Tutorial, Project]):

    # TODO: Right now this is super dumb, have to change this
    entries = []
    for subclass in entry_subclasses:
        entries += subclass.objects.order_by('-publishing_date').exclude(publishing_date__gte=timezone.now()).all()[0:n]

    print(entries)
    return entries

