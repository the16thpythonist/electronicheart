import os
from copy import deepcopy

from django.views.generic import TemplateView, View
from django.conf import settings
from django.urls import reverse_lazy
from django.shortcuts import render

from .cv import CV


def static_url(relative_path: str) -> str:
    return os.path.join(settings.STATIC_URL, relative_path)


class NavView(View):

    NAV_DEFAULT = {
        'home': {
            'label': 'Home',
            'active': False,
            'url': reverse_lazy('home')
        },
        'blog': {
            'label': 'The Blog',
            'active': False,
            'url': reverse_lazy('blog:entry_list')
        }
    }

    def __init__(self, *args, **kwargs):
        self.nav = deepcopy(self.NAV_DEFAULT)
        super(NavView, self).__init__(*args, **kwargs)

    def modify_context(self, context):
        context['nav'] = self.nav


class HomepageView(NavView):

    template = 'pages/home.html'

    def get(self, request):

        context = {
            'nav': self.nav
        }
        context.update(CV)
        context['nav']['home']['active'] = True

        return render(request, self.template, context=context)


