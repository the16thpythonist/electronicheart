from django.apps import AppConfig


class BlogAppConfig(AppConfig):

    name = 'blog'
    verbose_name = 'Blog'

    def ready(self):
        pass
