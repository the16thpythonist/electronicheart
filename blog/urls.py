from django.urls import path

from.models import Entry
from .views import EntryDetailView, JupyterNotebookDetailView
from .views import EntryListView, TutorialListView, ProjectListView, JupyterNotebookListView
from .views import DownloadJupyterNotebookView

app_name = "blog"

urlpatterns = [
    path('', view=EntryListView.as_view(), name='entry_list'),
    # OWN URLS
    path('tutorials/', view=TutorialListView.as_view(), name='tutorial_list'),
    path('tutorials/<slug:slug>/',
         view=EntryDetailView.as_view(),
         name=Entry.TYPE_TUTORIAL),
    path('projects/', view=ProjectListView.as_view(), name='project_list'),
    path('projects/<slug:slug>/',
         view=EntryDetailView.as_view(),
         name=Entry.TYPE_PROJECT),
    path('jupyter/', view=JupyterNotebookListView.as_view(), name='jupyter_list'),
    path('jupyter/<slug:slug>/',
         view=JupyterNotebookDetailView.as_view(),
         name=Entry.TYPE_JUPYTER),
    path('jupyter/<slug:slug>/download',
         view=DownloadJupyterNotebookView.as_view(),
         name='download_jupyter')
]
