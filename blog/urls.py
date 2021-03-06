from django.urls import path

from .views import TutorialDetailView

app_name = "blog"

urlpatterns = [
    # OWN URLS
    path('tutorials/<int:pk>/', view=TutorialDetailView.as_view(), name='tutorial_detail')
]
