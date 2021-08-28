from django.views.generic import View
from django.shortcuts import render, get_object_or_404

from .models import get_most_recent_entries
from .models import Entry, Tutorial, Project


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
            'object': project
        }
        return render(request, 'blog/project_detail.html', context)
