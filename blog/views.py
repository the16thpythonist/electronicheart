from django.views.generic import View
from django.shortcuts import render, get_object_or_404

from .models import get_most_recent_entries
from .models import Entry, Tutorial, Project, JupyterNotebook
from .models import Comment
from .forms import CommentForm

# == GENERAL POST VIEWS

class EntryListView(View):

    def get(self, request):
        entries = get_most_recent_entries(20)
        context = {
            'objects': entries
        }

        return render(request, 'blog/entry_list.html', context)


# == THE TUTORIAL POST TYPE SPECIFIC VIEWS

class TutorialDetailView(View):

    def get(self, request, slug):
        tutorial = get_object_or_404(Tutorial, slug=slug)
        context = {
            'object': tutorial
        }
        return render(request, 'blog/tutorial_detail.html', context)


class TutorialListView(View):

    def get(self, request):
        tutorials = Tutorial.get_most_recent(20)
        context = {
            'objects': tutorials
        }
        return render(request, 'blog/tutorial_list.html', context)


# == PROJECT POST TYPE SPECIFIC VIEWS

class ProjectDetailView(View):

    def get(self, request, slug):
        project = get_object_or_404(Project, slug=slug)
        context = {
            'object': project,
            'form': CommentForm()
        }
        return render(request, 'blog/project_detail.html', context)

    def post(self, request, slug):
        project = get_object_or_404(Project, slug=slug)
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
                entry=project
            )
            comment.save()

        context = {
            'object': project,
            'form': CommentForm()
        }
        return render(request, 'blog/project_detail.html', context)


class JupyterNotebookDetailView(View):

    def get(self, request, slug):
        obj = get_object_or_404(JupyterNotebook, slug=slug)
        context = {
            'object': obj
        }
        return render(request, 'blog/jupyter_detail.html', context)
