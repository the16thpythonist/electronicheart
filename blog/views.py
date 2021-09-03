import os
import datetime
from copy import deepcopy

from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse, Http404
# https://stackoverflow.com/questions/739776/how-do-i-do-an-or-filter-in-a-django-query
from django.db.models import Q

from .models import get_most_recent_entries, get_entries
from .models import Entry
from .models import Comment
from .forms import CommentForm
from electronicheart.views import NavView

# == GENERAL POST VIEWS


class BlogView(NavView):

    BLOG_NAV_DEFAULT = {
        'tutorial': {
            'active': False,
            'label': 'Tutorials',
            'url': reverse_lazy('blog:tutorial_list')
        },
        'project': {
            'active': False,
            'label': 'Projects',
            'url': reverse_lazy('blog:project_list')
        },
        'jupyter': {
            'active': False,
            'label': 'Jupyter Notebooks',
            'url': reverse_lazy('blog:jupyter_list')
        }
    }

    def __init__(self, *args, **kwargs):
        self.blog_nav = deepcopy(self.BLOG_NAV_DEFAULT)

        super(BlogView, self).__init__(*args, **kwargs)

    def get_context(self):
        self.nav['blog']['active'] = True
        return {
            'nav': self.nav,
            'blog_nav': self.blog_nav,
        }


class EntryDetailView(BlogView):

    model = Entry
    template = 'blog/entry_detail.html'

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug=slug)
        context = self.get_context()
        context['object'] = obj
        context['comment_form'] = CommentForm()
        self.modify_context(request, context)

        return render(request, self.template, context)

    def post(self, request, slug):
        obj = get_object_or_404(self.model, slug=slug)
        form = CommentForm(request.POST)

        # Adding a corresponding comment to the entry in case the form is correct
        if form.is_valid():
            comment = Comment(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                content=form.cleaned_data['content'],
                # I could do this inside the form actually if I dynamically add a new entry "active" to the
                # cleaned_data within the clean_content method without raising a validation error
                active=True,
                entry=obj
            )
            comment.save()

        context = self.get_context()
        context['object'] = obj
        context['comment_form'] = form
        self.modify_context(request, context)

        return render(request, self.template, context)

    def modify_context(self, request, context):
        pass


class JupyterNotebookDetailView(EntryDetailView):

    template = 'blog/jupyter_detail.html'

    def modify_context(self, request, context):
        print(context['object'].jupyter)

# == LIST VIEWS


class EntryListView(BlogView):

    template = 'blog/entry_list.html'
    entry_count = 20
    filter_kwargs = {}

    def get(self, request):
        context = self.get_context()
        context['title'] = 'Recent Posts'

        self.modify_context(request, context)
        return render(request, self.template, context)

    def modify_context(self, request, context: dict):

        # If there are additional get parameters than we need to do fancy stuff because that means that the user has
        # potentially used the search form or requests older posts specifically. If that is not the case then we
        # we simply can return the most recent posts
        if request.GET:

            if 'older' in request.GET:
                older_date = request.GET['older']
                entries = Entry.objects.filter(publishing_date__lte=older_date,
                                               **self.filter_kwargs)\
                                       .order_by('-publishing_date')[:self.entry_count]
                context['objects'] = entries
                context['title'] += f'<br>older than: {older_date}'
                context['oldest'] = entries[-1].publishing_date
                return

            if 'search' in request.GET:
                search_string = request.GET['search']
                # Most important are titles
                entries = Entry.objects.filter(Q(title__icontains=search_string) |
                                               Q(subtitle__icontains=search_string)).all()

                # And only then we want to list the "semi related" posts which contain the search in the fulltext
                entries += Entry.objects.filter(text__icontains=search_string).all()
                context['objects'] = entries
                context['title'] += f'<br>search: "{search_string}"'
                return

        # Since the special cases return this is the default operation if none of these special cases is present.
        entries = Entry.objects.filter(publishing_date__lte=datetime.datetime.now(),
                                       **self.filter_kwargs)\
                               .order_by('-publishing_date')[:self.entry_count]
        context['objects'] = entries
        context['oldest'] = entries[-1].publishing_date
        print(context['oldest'])


class TutorialListView(EntryListView):

    filter_kwargs = {'type': Entry.TYPE_TUTORIAL}

    def modify_context(self, request, context):
        super(TutorialListView, self).modify_context(request, context)
        context['blog_nav']['tutorial']['active'] = True
        context['title'] = 'Tutorials'


class ProjectListView(EntryListView):

    filter_kwargs = {'type': Entry.TYPE_PROJECT}

    def modify_context(self, request, context):
        super(ProjectListView, self).modify_context(request, context)
        context['blog_nav']['project']['active'] = True
        context['title'] = 'Projects'


class JupyterNotebookListView(EntryListView):

    filter_kwargs = {'type': Entry.TYPE_JUPYTER}

    def modify_context(self, request, context):
        super(JupyterNotebookListView, self).modify_context(request, context)
        context['blog_nav']['jupyter']['active'] = True
        context['title'] = 'Jupyter Notebooks'


# == SPECIAL VIEWS

class DownloadJupyterNotebookView(View):
    """
    This view is used to download the actual jupyter notebook files belonging to a corresponding instance of the
    JupyterNotebook model. This view does not respond with a html string but instead the raw content of the file, which
    prompts the browser to download it.

    **THE IDEA**
    So what I want to do is this: I want to have a button beneath a jupyter notebook post which allows to download
    the actual jupyter notebook file so that an interested visitor may play around with it themselves.
    To achieve this I would have to do this: I need a separate URL endpoint whose link I will put onto the button.
    This endpoint will not respond with a html string (which represents a web page) but instead a special http payload
    which tells the browser that I am trying to make it download a file.

    https://stackoverflow.com/questions/62479933/enabling-a-django-download-button-for-pdf-download
    """

    def get(self, request, slug):
        notebook = get_object_or_404(Entry, slug=slug)

        # TODO: At some point I think I also want to enable ZIP files here and I would have to add a if clause for
        #       differing content types.
        with open(notebook.jupyter_file.path) as file:
            content = file.read()
            response = HttpResponse(content, content_type='application/x-ipynb')
            response['Content-Disposition'] = f'inline; filename={os.path.basename(notebook.jupyter_file.path)}'
            return response
