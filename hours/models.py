import datetime

import matplotlib.pyplot as plt
from django.db import models
from filer.fields.image import FilerImageField, FilerFileField
from django.core.files import File
from filer.models import Image

from .harvest import (HarvestApi,
                      create_projects_dict,
                      plot_daily_hours_over_timespan,
                      plot_project_total_over_timespan,
                      plot_weekly_total_by_project,
                      get_week_by_day,
                      get_projects_total_over_timespan)


# Create your models here.
class DailyStatistics(models.Model):

    id = models.AutoField(primary_key=True)
    date = models.DateField(unique=True)
    hours_today = models.FloatField(null=True, default=1.0)
    hours_total = models.FloatField(null=True, default=1.0)
    daily_hours_plot = FilerImageField(related_name="daily_hours", on_delete=models.CASCADE, null=True)
    weekly_hours_plot = FilerImageField(related_name="weekly_hours", on_delete=models.CASCADE, null=True)

    @classmethod
    def update(cls, date: datetime.date):
        # 1. Fetch all the data from the harvest api and populate the projects dict
        api = HarvestApi()
        time_entries = api.get_all_time_entries()
        projects_dict = create_projects_dict(time_entries)

        # 2. Creating the daily hours plot
        week = get_week_by_day(
            datetime.datetime.combine(
                date,
                datetime.datetime.min.time()
            )
        )
        week_start = week[0]
        week_end = week[-1]
        date_datetime = datetime.datetime.combine(date, datetime.datetime.min.time())

        fig, (ax1, ax2) = plt.subplots(
            nrows=2,
            ncols=1,
            figsize=(12, 12),
            gridspec_kw={
                'height_ratios': [2, 1]
            }
        )
        plot_daily_hours_over_timespan(
            axes=ax1,
            projects_dict=projects_dict,
            start_datetime=week_start,
            end_datetime=week_end
        )
        plot_project_total_over_timespan(
            axes=ax2,
            projects_dict=projects_dict,
            start_datetime=week_start,
            end_datetime=week_end
        )

        daily_plot_file_name = 'daily.png'
        daily_plot_file_path = f'/tmp/{daily_plot_file_name}'

        fig.savefig(daily_plot_file_path)

        # https://stackoverflow.com/questions/20635332/how-to-programmatically-fill-or-create-filer-fields-image-filerimagefield
        with open(daily_plot_file_path, mode='rb') as file:
            file_obj = File(file, name=daily_plot_file_name)
            daily_plot_image = Image.objects.create(
                original_filename=daily_plot_file_name,
                file=file_obj
            )

        # 3. Creating the plot for the weekly hours
        fig, ax = plt.subplots(
            nrows=1,
            ncols=1,
            figsize=(12, 12)
        )

        plot_weekly_total_by_project(
            axes=ax,
            projects_dict=projects_dict,
            start_datetime=datetime.datetime.combine(date, datetime.datetime.min.time()) - datetime.timedelta(weeks=6),
            end_datetime=datetime.datetime.combine(date, datetime.datetime.min.time())
        )

        weekly_plot_file_name = 'weekly.png'
        weekly_plot_file_path = f'/tmp/{weekly_plot_file_name}'

        fig.savefig(weekly_plot_file_path)

        # https://stackoverflow.com/questions/20635332/how-to-programmatically-fill-or-create-filer-fields-image-filerimagefield
        with open(weekly_plot_file_path, mode='rb') as file:
            file_obj = File(file, name=weekly_plot_file_name)
            weekly_plot_image = Image.objects.create(
                original_filename=weekly_plot_file_name,
                file=file_obj
            )

        # 4. Computing the single stat values
        projects_today = get_projects_total_over_timespan(
            projects_dict=projects_dict,
            start_datetime=datetime.datetime.combine(date, datetime.datetime.min.time()),
            end_datetime=datetime.datetime.combine(date, datetime.datetime.min.time())
        )
        hours_today = sum(projects_today.values())

        projects_total = get_projects_total_over_timespan(
            projects_dict=projects_dict,
            start_datetime=datetime.datetime(year=1, month=1, day=1),
            end_datetime=datetime.datetime.combine(date, datetime.datetime.min.time())
        )
        hours_total = sum(projects_total.values())

        # 5. Creating the new object
        cls.objects.update_or_create(
            date=date,
            defaults={
                'hours_today': hours_today,
                'hours_total': hours_total,
                'daily_hours_plot': daily_plot_image,
                'weekly_hours_plot': weekly_plot_image
            }
        )
