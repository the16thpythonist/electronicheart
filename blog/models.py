from __future__ import annotations
import datetime
from typing import List, Type, Sequence, Dict, Any, Callable

from django.db import models
from django.db.models import (SlugField,
                              CharField,
                              TextField,
                              DateTimeField,
                              URLField,
                              ForeignKey,
                              BooleanField,
                              Choices)
from django.utils import timezone
from django.utils.text import slugify
from django.utils.decorators import classproperty
from django.urls import reverse_lazy
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.templatetags.static import static

from filer.fields.image import FilerImageField, FilerFileField
from bs4 import BeautifulSoup

from electronicheart.users.models import User
from .apps import BlogAppConfig


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
    email = models.EmailField()
    content = TextField(max_length=2000, blank=True)
    publishing_date = DateTimeField(default=timezone.now)

    # These two will not be settable manually.
    # The "hash_id" is an integer hash value which is computed from the name of the comment (the pseudonym the author
    # chooses) and the entered email address.
    # In the first step, the author field can only be manipulated from the admin backend which means that only
    # registered admins could change this.
    hash_id = models.CharField(max_length=3, null=True, blank=True)
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

    @property
    def html(self):
        return self.content.replace('\n', '<br>')

    def save(self, *args, **kwargs):
        if not self.hash_id:
            self.hash_id = self.generate_hash_id()

        return super(Comment, self).save(*args, **kwargs)

    def get_image_url(self):
        if self.author:
            return self.author.image.url

        image_file = f'comment_images/{self.hash_id}.jpg'
        return static(image_file)

    def generate_hash_id(self) -> str:
        hash_base = f'{self.name} - {self.email.lower()}'
        hash_string = str(hash(hash_base))
        hash_id = hash_string[-3:]
        return hash_id

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



"""
**REWORKING THE ENTRY MODEL**

So this has been a learning experience. Here is how my first attempt at the models looked like: I had an *abstract*
base model "Entry" as one class and then several classes "Tutorial", "Project", "JupyterNotebook" which all inherited
from this base class and implemented actual models. I thought this was a good approach since this is how you would be
encouraged to do it with usual object oriented programming. All these specific classes have a lot in common but some
differences.

Now I have come to the painful realization, that this is actually BAD. I have been thinking in terms of object
orientation, but these classes model the tables of a relational database. The ORM only makes it seem like it is related
to object orientation. In the database model the inheritance thing doesnt really translate. One huge problem is that
there is no way of querying against the general "entry" type. For some cases I would like to search over all entries
and thats just not possible. The fact that the database sees these as more or less fundamentally different models is
that producing a general template only kind of works with a bit of hackery and implicit assumptions...

So I will have to change the whole way the models work. My plan would be to have only a single "Entry" model and then
differentiate the types by using a ChoiceField. Now with this approach there are other complications then: The jupyter
entry type is for example extremely different in the sense that it requires a bunch more fields. My plan for that would
be to have an additional model JupyterExtension, put the fields there and make an optional one-to-one relationship.
In the templates I'll have to render these extension fields then conditionally based on the type. Another thing which
causes me some headache is how to do the admin section in that case then but that is not as big of a problem if it does
not work out as the way it is now in general.
"""


class Entry(models.Model):

    TYPE_TUTORIAL = 'tutorial'
    TYPE_PROJECT = 'project'
    TYPE_JUPYTER = 'jupyter'

    TYPE_CHOICES = (
        (TYPE_TUTORIAL, 'Tutorial'),
        (TYPE_PROJECT, 'Project'),
        (TYPE_JUPYTER, 'Jupyter Notebook')
    )

    ICON_MAP = {
        TYPE_TUTORIAL: '<i class="fa fa-graduation-cap"></i>',
        TYPE_PROJECT: '<i class="fa fa-bolt"></i>',
        TYPE_JUPYTER: '<i class="fa fa-code"></i>',
    }

    type = CharField(max_length=10,
                     choices=TYPE_CHOICES)
    title = CharField(max_length=250,
                      help_text='The main title of the entry. Does not have to be unique')
    subtitle = CharField(max_length=250, default='', blank=True)
    description = CharField(max_length=200, default='', blank=True)
    author = ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='tutorials')
    thumbnail = FilerImageField(related_name="tutorial_thumbnail", on_delete=models.CASCADE, null=True)

    slug = SlugField(max_length=250, default='auto', unique=True)

    content = TextField(default='')
    text = TextField(default='')

    publishing_date = DateTimeField(default=timezone.now)
    creation_date = DateTimeField(default=timezone.now)

    next = URLField(null=True, blank=True)
    previous = URLField(null=True, blank=True)

    comments = GenericRelation(Comment)

    def save(self, *args, **kwargs) -> None:
        if self.slug == 'auto':
            self.slug = slugify(self.title)

        # So we need the "text" property to literally just contain the content of the post in all lower case and
        # without all the html markup (this will be used for fulltext search of keywords). BeautifulSoup does this
        # really well natively.
        soup = BeautifulSoup(self.content, 'lxml')
        self.text = soup.text.lower()

        super(Entry, self).save(*args, **kwargs)

    @classmethod
    def get_most_recent(cls, n: int) -> List[Entry]:

        entries = cls.objects.order_by('-publishing_date').exclude(publishing_date__gte=timezone.now()).all()[0:n]

        return entries

    @property
    def comment_count(self):
        return len(self.comments.filter(active=True))

    @property
    def fa_icon(self):
        return self.ICON_MAP[self.type]

    @property
    def url(self) -> str:
        """
        Returns the absolute URL of the detail view of the entry instance.

        :return:
        """
        # This is a bit hacky (because it technically stretches the limits of SOC a bit) but very convenient!
        # Here is the thing: This is an abstract base model which will be the base for multiple specific
        # implementations, but we want a common list view for those and a list view would need knowledge of the urls
        # of the detail pages to link to those correctly. Thus we need a generalized method for getting those aka
        # we cannot do the {% url "..." %} thing because for that we need to provide a *specific* model type, which we
        # generally do not know at that point since it could be any specific implementation. Sooo it would be better if
        # the url information for the detail page would be attached to every individual element right away <- this
        # property.
        # Now this only works because of an implicit assumption we make: In the "url.py" module we set the name of
        # the according detail view for a model to the "type" property of the corresponding model class. If we adhere
        # to this convention, we can make use of it here and already assemble all the information to let django reverse
        # the url for a specific Entry instance...
        view_name = f'{BlogAppConfig.name}:{self.type}'
        return reverse_lazy(view_name, kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.type.upper()}: {self.title}'


class JupyterNotebookExtension(models.Model):

    entry = models.OneToOneField(Entry, on_delete=models.CASCADE, related_name='jupyter')
    # TODO: In the future I might be able to make it such that the user only needs to provide the ipynb file and the
    #       the conversion is done automatically.
    # TODO: Maybe there is a way to check if the files have the correct file extensions and such?
    # So when creating a new "jupyter" post, the user needs to provide two files: The actual juypter notebook file
    # (this will only be necessary for letting the user download the file to try out themselves) and the html file
    # which was exported from the notebook. The idea is that the html file is parsed and the relevant html parts are
    # then rendered in the django post template.
    jupyter_file = FilerFileField(on_delete=models.CASCADE, related_name='jupyter_file')
    html_file = FilerFileField(on_delete=models.CASCADE, related_name='html_file')

    # These two fields should contain the html code which actually represents the jupyter notebook. These should NOT
    # be manually settable, they are automatically derived from the html file.
    head_html = TextField(null=True, blank=True)
    content_html = TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.html_file:
            with open(self.html_file.path, mode='r') as file:
                html_string = file.read()

            soup = BeautifulSoup(html_string, 'html.parser')
            self.head_html = str(soup.head)
            self.content_html = str(soup.find(id='notebook'))

        return super(JupyterNotebookExtension, self).save(*args, **kwargs)

"""
class Tutorial(Entry):

    type = 'tutorial'
    fa_icon = '<i class="fa fa-graduation-cap"></i>'
    author = ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='tutorials')
    thumbnail = FilerImageField(related_name="tutorial_thumbnail", on_delete=models.CASCADE, null=True)


class Project(Entry):

    type = 'project'
    fa_icon = '<i class="fa fa-bolt"></i>'
    author = ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='projects')
    thumbnail = FilerImageField(related_name='project_thumbnail', on_delete=models.CASCADE, null=True)


class JupyterNotebook(Entry):

    type = 'jupyter'
    author = ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='jupyter_notebooks')
    thumbnail = FilerImageField(related_name="jupyter_thumbnail", on_delete=models.CASCADE, null=True)

    # TODO: In the future I might be able to make it such that the user only needs to provide the ipynb file and the
    #       the conversion is done automatically.
    # TODO: Maybe there is a way to check if the files have the correct file extensions and such?
    # So when creating a new "jupyter" post, the user needs to provide two files: The actual juypter notebook file
    # (this will only be necessary for letting the user download the file to try out themselves) and the html file
    # which was exported from the notebook. The idea is that the html file is parsed and the relevant html parts are
    # then rendered in the django post template.
    jupyter_file = FilerFileField(on_delete=models.CASCADE, related_name='jupyter_file')
    html_file = FilerFileField(on_delete=models.CASCADE, related_name='html_file')

    # These two fields should contain the html code which actually represents the jupyter notebook. These should NOT
    # be manually settable, they are automatically derived from the html file.
    head_html = TextField(null=True, blank=True)
    content_html = TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.html_file:
            with open(self.html_file.path, mode='r') as file:
                html_string = file.read()

            soup = BeautifulSoup(html_string, 'html.parser')
            self.head_html = str(soup.head)
            self.content_html = str(soup.find(id='notebook'))

        return super(JupyterNotebook, self).save(*args, **kwargs)
"""

# == UTILITY FUNCTIONS

def get_most_recent_entries(n: int,
                            entry_subclasses: List[type] = []):

    # TODO: Right now this is super dumb, have to change this
    entries = []
    for subclass in entry_subclasses:
        entries += subclass.objects.order_by('-publishing_date').exclude(publishing_date__gte=timezone.now()).all()[0:n]

    print(entries)
    return entries


"""
**HOW DO I QUERY THE ENTRIES?**

So I have run into a problem: I have effectively three separate models which I would like to treat as one thing in some
cases and as their own thing in other cases. This sucks a little bit.
"""


def get_entries(n: int,
                entry_subclasses: List[Type[Entry]] = [],
                filter_args: List[Any] = [],
                filter_kwargs: Dict[str, Any] = {},
                order_args: List[str] = [],
                sort_callback: Callable = lambda l: l):

    entries = []
    for subclass in entry_subclasses:
        queryset = subclass.objects.filter(*filter_args, **filter_kwargs).order_by(*order_args)
        if n > 0:
            queryset = queryset[:n]
        entries += list(queryset)

    entries = sort_callback(entries)

    if len(entries) >= n and n > 0:
        entries = entries[:n]

    return entries
