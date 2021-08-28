from django.urls import path

from .views import EntryListView
from .views import TutorialDetailView, TutorialListView
from .views import ProjectDetailView

app_name = "blog"

urlpatterns = [
    path('', view=EntryListView.as_view(), name='entry_list'),
    # OWN URLS
    path('tutorials/', view=TutorialListView.as_view(), name='tutorial_list'),
    path('tutorials/<slug:slug>/', view=TutorialDetailView.as_view(), name='tutorial_detail'),
    path('projects/<slug:slug>/', view=ProjectDetailView.as_view(), name='project_detail')
]
