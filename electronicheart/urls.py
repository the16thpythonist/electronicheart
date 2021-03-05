from django.urls import path
from django.views.generic import TemplateView
from electronicheart.views import HomepageView

app_name = "electronicheart"

urlpatterns = [
    path(
        "",
        HomepageView.as_view(),
        name="home",
    ),
]
