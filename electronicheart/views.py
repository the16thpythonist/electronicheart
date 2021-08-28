import os

from django.views.generic import TemplateView
from django.conf import settings

from .cv import CV


def static_url(relative_path: str) -> str:
    return os.path.join(settings.STATIC_URL, relative_path)


class HomepageView(TemplateView):

    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        context.update(CV)

        return context


