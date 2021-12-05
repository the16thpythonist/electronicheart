from django.urls import path
from django.views.generic import TemplateView
from .views import WorkingHoursView

app_name = "hours"

urlpatterns = [
    path(
        "",
        WorkingHoursView.as_view(),
        name="hours",
    )
]
