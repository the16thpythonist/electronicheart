from __future__ import annotations
import datetime
from typing import List

from django.db import models
from django.db.models import (SlugField,
                              CharField,
                              TextField,
                              DateTimeField,
                              URLField,
                              ForeignKey,
                              BooleanField)
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from filer.fields.image import FilerImageField

from electronicheart.users.models import User


# == ACTUAL MODEL CLASSES

# Note: The "Comment" class actually has to be defined first. The comment model realizes it's foreign key relations
# using the contenttypes api as a "generic relation". This means that you dont have to specify to which model type this
# relation goes, it could be any. Now this also means you cannot simply do "related_name", but rather in this case you
# have to do it the other way around: Explicitly declare a relation from the "one" side of the "one-to-many"
# relationship. And to be able to do this the class "Comment" obviously has to be already defined.

class Comment(models.Model):
    """
    This model represents a comment which can be added to any post by an anonymous visitor
    """
    name = CharField(max_length=250)
    # TODO: Remove the default!
    email = models.EmailField(default="max.mustermann@gmail.com")
    content = TextField(max_length=2000, blank=True)
    publishing_date = DateTimeField(default=timezone.now)

    # These two will not be settable manually.
    # The "hash_id" is an integer hash value which is computed from the name of the comment (the pseudonym the author
    # chooses) and the entered email address.
    # In the first step, the author field can only be manipulated from the admin backend which means that only
    # registered admins could change this.
    hash_id = models.BigIntegerField(null=True, blank=True)
    author = ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # https://docs.djangoproject.com/en/3.2/ref/contrib/contenttypes/x
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    entry = GenericForeignKey('content_type', 'object_id')

    # This is intended to at some point help with moderating. The idea is to have a filter check for obvious problems
    # with the comments like swearing etc. and then automatically set active to false, which means they wont be
    # displayed and wait for further approval in the admin backend.
    active = BooleanField(default=False)

    # So here are my thoughts about images: I think anonymous commenters pose quite the problem: Beside the usual stuff
    # like spamming etc. I am worried about identity theft: On default someone could just copy the comment name of
    # someone else and pretend that it is the same person. So the plan is to also have the commenter enter the email
    # address for every comment and then build a hash value from the public comment name and the email address which is
    # only saved on the server. Based on this hash value (there will be relatively few possible values) a specific Anon
    # profile picture will be set. This will ensure that the same person could be identified by the profile picture.
    image = FilerImageField(on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.hash_id:
            self.hash_id = self.generate_hash_id()

        return super(Comment, self).save(*args, **kwargs)

    def generate_hash_id(self) -> int:
        hash_base = f'{self.name} - {self.email}'
        return hash(hash_base)

    def get_shortened_content(self, length=30) -> str:
        """
        Returns the first *length* characters of the content string of the comment. If the comment is shorter than this
        length, returns the whole content instead.

        :param length: The int amount of the first characters of the content to return
        :return:
        """
        if len(self.content) <= length:
            return self.content
        else:
            shortened_content = self.content[0:length] + '...'
            return shortened_content

    # This is curious: We assign a property "short_description" to the method instance. This is made to support the
    # usage of this method in the admin form list display. If the function has this "short description" string property
    # then this string will be displayed as the title of the column in the list display.
    get_shortened_content.short_description = 'Content'


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

    comments = GenericRelation(Comment)

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

