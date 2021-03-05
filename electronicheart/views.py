import os

from django.views.generic import TemplateView
from django.conf import settings


def static_url(relative_path: str) -> str:
    return os.path.join(settings.STATIC_URL, relative_path)


class HomepageView(TemplateView):

    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        print("HELLO")
        context = super(HomepageView, self).get_context_data(**kwargs)

        context['programming_abilities'] = [
            [
                {
                    'name': 'Python',
                    'rating': [1, 1, 1, 1, 1],
                    'icon_url': 'https://python.org/static/favicon.ico'
                },
                {
                    'name': 'Click',
                    'rating': [1, 1, 1, 1, 0],
                    'icon_url': static_url('images/favicons/click.ico')
                },
                {
                    'name': 'Django',
                    'rating': [1, 1, 1, 0, 0],
                    'icon_url': static_url('images/favicons/django.ico')
                },
                {
                    'name': 'Flask',
                    'rating': [1, 1, 0, 0, 0],
                    'icon_url': static_url('images/favicons/flask.ico')
                }
            ],
            [
                {
                    'name': 'HTML5',
                    'rating': [1, 1, 1, 1, 0],
                    'icon_url': static_url('images/favicons/html.ico')
                },
                {
                    'name': 'CSS',
                    'rating': [1, 1, 1, 1, 0],
                    'icon_url': static_url('images/favicons/css.ico')
                },
                {
                    'name': 'Javascript',
                    'rating': [1, 1, 1, 0, 0],
                    'icon_url': static_url('images/favicons/js.ico')
                },
                {
                    'name': 'VueJS',
                    'rating': [1, 1, 0, 0, 0],
                    'icon_url': static_url('images/favicons/vue.ico')
                },
                {
                    'name': 'PHP',
                    'rating': [1, 1, 1, 0, 0],
                    'icon_url': static_url('images/favicons/php.ico')
                },
                {
                    'name': 'Wordrpess',
                    'rating': [1, 1, 0, 0, 0],
                    'icon_url': static_url('images/favicons/wordpress.ico')
                }
            ]
        ]
        context['projects'] = [
            {
                'name': 'Schiller in Space',
                'image_url': static_url('images/ipe.jpg')
            },
            {
                'name': 'UcaPhantom',
                'image_url': static_url('images/ipe.jpg')
            },
            {
                'name': 'UfoTest',
                'image_url': static_url('images/ipe.jpg')
            }
        ]
        context['contacts'] = [
            {
                'content': 'jonseb1998@gmail.com',
                'href': '/',
                'image_url': static_url('images/favicons/favicon.ico')
            }
        ]

        return context
