from copy import deepcopy

from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from .models import get_most_recent_entries
from .models import Entry, Tutorial, Project, JupyterNotebook
from .models import Comment
from .forms import CommentForm

# == GENERAL POST VIEWS


class BlogView(View):

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


class EntryDetailView(BlogView):

    model = Entry
    template = 'blog/entry_detail.html'

    def get(self, request, slug):
        obj = get_object_or_404(self.model, slug=slug)
        context = {
            'object': obj,
            'blog_nav': self.blog_nav,
            'comment_form': CommentForm()
        }

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

        context = {
            'object': obj,
            'blog_nav': self.blog_nav,
            'comment_form': CommentForm()
        }
        return render(request, self.template, context)


class TutorialDetailView(EntryDetailView):

    model = Tutorial
    template = 'blog/entry_detail.html'


class ProjectDetailView(EntryDetailView):

    model = Project
    template = 'blog/entry_detail.html'


class JupyterNotebookDetailView(EntryDetailView):

    model = JupyterNotebook
    template = 'blog/jupyter_detail.html'


# == LIST VIEWS


class EntryListView(BlogView):

    template = 'blog/entry_list.html'

    def get(self, request):
        context = {
            'objects': [],
            'blog_nav': self.blog_nav,
            'title': 'Recent Posts'
        }
        self.modify_context(request, context)
        return render(request, self.template, context)

    def modify_context(self, request, context: dict):
        context['objects'] = get_most_recent_entries(20)


class TutorialListView(EntryListView):

    def modify_context(self, request, context):
        context['blog_nav']['tutorial']['active'] = True
        context['objects'] = Tutorial.get_most_recent(20)
        context['title'] = 'Tutorials'


class ProjectListView(EntryListView):

    def modify_context(self, request, context):
        context['blog_nav']['project']['active'] = True
        context['objects'] = Project.get_most_recent(20)
        context['title'] = 'Projects'


class JupyterNotebookListView(EntryListView):

    def modify_context(self, request, context):
        context['blog_nav']['jupyter']['active'] = True
        context['objects'] = JupyterNotebook.get_most_recent(20)
        context['title'] = 'Jupyter Notebooks'
