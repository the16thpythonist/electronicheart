import datetime

from django.shortcuts import render
from django.core.files import File
from filer.models import Image

from electronicheart.views import NavView
from .harvest import HarvestApi, yesterday
from .models import DailyStatistics


class WorkingHoursView(NavView):

    template = 'pages/hours.html'

    def get(self, request):

        if not DailyStatistics.objects.filter(date=yesterday()).exists():
            # Create a new object if none exists
            DailyStatistics.update(yesterday())

        daily_statistics = DailyStatistics.objects.get(date=yesterday())

        context = {
            'nav': self.nav,
            'object': daily_statistics
        }

        return render(request, self.template, context=context)


