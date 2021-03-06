from django.views.generic import View
from django.shortcuts import render, get_object_or_404

from .models import Tutorial


class TutorialDetailView(View):

    def get(self, request, pk):
        tutorial = get_object_or_404(Tutorial, pk=pk)
        context = {
            'object': tutorial
        }
        return render(request, 'blog/tutorial_detail.html', context)
