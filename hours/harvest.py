import requests
import os
import copy
import datetime
from collections import defaultdict
from typing import List

from django.conf import settings

import matplotlib.pyplot as plt
import matplotlib.lines as lns


# === UTILITY FUNCTIONS

def yesterday() -> datetime.date:
    today = datetime.date.today()
    return today - datetime.timedelta(days=1)


def get_week_by_day(reference_datetime: datetime.datetime) -> List[datetime.datetime]:
    reference_datetime = datetime.datetime(year=reference_datetime.year,
                                           month=reference_datetime.month,
                                           day=reference_datetime.day)
    week_datetimes = [reference_datetime]

    for i in range(1, reference_datetime.weekday() + 1):
        _datetime = reference_datetime - datetime.timedelta(days=i)
        week_datetimes = [_datetime] + week_datetimes

    for j in range(1, 6 - reference_datetime.weekday() + 1):
        _datetime = reference_datetime + datetime.timedelta(days=j)
        week_datetimes = week_datetimes + [_datetime]

    return week_datetimes


# === DATA PROCESSING

class HarvestApi:

    def __init__(self):
        self.headers = {
            'Authorization': f'Bearer {settings.HARVEST_ACCESS_TOKEN}',
            'Harvest-Account-Id': f'{settings.HARVEST_ACCOUNT_ID}',
            'User-Agent': 'Electronic Heart'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.url = settings.HARVEST_API_URL

    def get(self, endpoint: str, params: dict = {}) -> requests.Response:
        """

        :raises requests.exceptions.HTTPError: In case the request is invalid, meaning the response has a non
            2xx status code!
        :param endpoint:
        :param params:
        :return:
        """
        url = os.path.join(self.url, endpoint)
        print(self.url)
        print(url)
        response = self.session.get(url, params=params)

        return response

    def get_all_time_entries(self) -> List[dict]:
        """
        Fetches and returns a list of all time entry objects from the api.

        :return:
        """
        time_entries = []

        next_page = 1
        while next_page is not None:
            try:
                response = self.get('time_entries', {'page': next_page})
                # This method will make the response actually raise an exception if the response status is not 2xx!
                # Usually the get call would not do this and only raise an error if there was an actual timeout or smth
                # like that. I like this, since it explicitly forces the top layers to handle a bad return.
                response.raise_for_status()

                data = response.json()
                time_entries += data['time_entries']
                next_page = data['next_page']
            except requests.exceptions.HTTPError as e:
                print('Harvest Error: ' + str(e))
                break

        return time_entries


def create_projects_dict(time_entries: List[dict]) -> dict:
    projects_dict = copy.deepcopy(settings.HARVEST_PROJECTS)

    # 1.Adding the raw time entry list to each project
    for project_id, project_data in projects_dict.items():
        project_data['time_entries'] = [time_entry
                                        for time_entry in time_entries
                                        if (time_entry['project']['name'], time_entry['task']['name']) == project_id]

    # 2.We want a processed data structure from these raw entries which tells us the cumulative time spent
    # per project and per day.
    for project_id, project_data in projects_dict.items():
        daily_hours = defaultdict(float)

        for time_entry in project_data['time_entries']:
            date = time_entry['spent_date']
            daily_hours[date] += time_entry['hours']

        project_data['daily_hours'] = dict(daily_hours)

    return projects_dict


def get_projects_total_over_timespan(projects_dict: dict,
                                     start_datetime: datetime.datetime,
                                     end_datetime: datetime.datetime):
    projects_total = {project_id: 0 for project_id in projects_dict.keys()}

    for project_id, project_data in projects_dict.items():

        for date_string, hours in project_data['daily_hours'].items():
            _datetime = datetime.datetime.strptime(date_string, settings.HARVEST_DATETIME_FORMAT)
            if start_datetime <= _datetime <= end_datetime:
                projects_total[project_id] += hours

    return projects_total


# === CREATING OF PLOTS


def plot_daily_hours_over_timespan(axes: plt.Axes,
                                   projects_dict: dict,
                                   start_datetime=datetime.datetime.now(),
                                   end_datetime=datetime.datetime.now(),
                                   ) -> plt.Axes:

    # ~ Populating the plot
    dts = [(start_datetime + datetime.timedelta(days=offset))
           for offset in range((end_datetime - start_datetime).days + 1)]

    for index, dt in enumerate(dts, start=1):

        date_string = dt.strftime(settings.HARVEST_DATETIME_FORMAT)
        previous_hours = 0
        for project_id, project_data in projects_dict.items():
            if date_string in project_data['daily_hours']:
                hours = project_data['daily_hours'][date_string]
                axes.bar(x=index,
                         bottom=previous_hours,
                         height=hours,
                         color=project_data['color'])

                previous_hours += hours

        axes.text(x=index,
                  y=previous_hours + 0.1,
                  s=f'{previous_hours:0.2f}',
                  fontsize='large',
                  ha='center')

    # ~ Additional plot info
    yticks = list(range(1, len(dts) + 1))
    axes.set_xlim(yticks[0] - 0.5, yticks[-1] + 0.5)
    axes.set_xticks(yticks)
    axes.set_xticklabels([dt.strftime('%d.%m.%Y\n(%A)') for dt in dts])
    axes.set_ylim(0, 12)
    axes.set_title('Daily hours')

    custom_lines = []
    custom_labels = []
    for project_id, project_data in projects_dict.items():
        custom_lines.append(lns.Line2D([0], [0], color=project_data['color'], lw=3))
        custom_labels.append(project_data['label'])
    axes.legend(custom_lines, custom_labels)

    return axes


def plot_project_total_over_timespan(axes: plt.Axes,
                                     projects_dict: dict,
                                     start_datetime=datetime.datetime.now(),
                                     end_datetime=datetime.datetime.now()
                                     ) -> plt.Axes:
    # Convenience feature: The start and end datetime can be given as strings, as that
    # is often a lot easier for the user. These will be automatically converted into
    # datetime objects
    datetime_format = '%Y-%m-%d'
    if isinstance(start_datetime, str):
        start_datetime = datetime.datetime.strptime(start_datetime, datetime_format)
    if isinstance(end_datetime, str):
        end_datetime = datetime.datetime.strptime(end_datetime, datetime_format)

    # ~ Population plot
    projects_total = defaultdict(float)
    for index, (project_id, project_data) in enumerate(projects_dict.items(), start=1):

        for date_string, hours in project_data['daily_hours'].items():
            dt = datetime.datetime.strptime(date_string, datetime_format)
            if start_datetime <= dt <= end_datetime:
                projects_total[project_id] += hours

        # Now after the previous loop over all entries of daily working hours
        # have been processed we can plot the final value for the current project
        total_hours = projects_total[project_id]
        axes.barh(y=index,
                  width=total_hours,
                  label=project_data['label'],
                  color=project_data['color'])

        # Besides the bar itself there will also be a text label with the actual value
        axes.text(y=index,
                  x=total_hours + 0.05,
                  s=f'{total_hours:0.2f}',
                  fontsize='large',
                  va='center')

    # ~ Additional plot info
    total_hours = sum(hours for hours in projects_total.values())
    max_hours = max(hours for hours in projects_total.values())
    axes.set_title(f'Total hours: {total_hours:0.2f}')
    axes.set_yticks(list(range(1, len(projects_total) + 1)))
    axes.set_yticklabels([d['label'] for d in projects_dict.values()])
    axes.set_xlabel('time in hours')
    axes.set_xlim(0, max_hours + 2)
    axes.legend()

    return axes


def plot_weekly_total_by_project(axes: plt.Axes,
                                 projects_dict: dict,
                                 start_datetime: datetime.datetime,
                                 end_datetime: datetime.datetime,
                                 datetime_format: str = '%Y-%m-%d',
                                 cumulative_color=(0, 0, 0, 0.1)):
    # ~ Generating the weeks
    current_week = get_week_by_day(start_datetime)
    weeks = [current_week]
    while current_week[-1] < end_datetime:
        current_week = [dt + datetime.timedelta(weeks=1) for dt in current_week]
        weeks.append(current_week)

    # ~ Populating the plot
    axes_total = axes.twinx()
    # axes_total, axes = axes, axes_total

    projects_weekly_total = defaultdict(list)
    indices = list(range(1, len(weeks) + 1))
    for index, week in zip(indices, weeks):

        projects_total = get_projects_total_over_timespan(projects_dict,
                                                          start_datetime=week[0],
                                                          end_datetime=week[-1])
        print(list(projects_dict.values())[0].keys())
        print(week[0], week[1], projects_total)
        for project_id, project_data in projects_dict.items():
            weekly_total = projects_total[project_id]
            projects_weekly_total[project_id].append(weekly_total)
            axes.scatter(x=index,
                         y=weekly_total,
                         color=project_data['color'],
                         lw=3)

        total = sum(hours for hours in projects_total.values())
        axes_total.bar(x=index,
                       height=total,
                       width=0.4,
                       color=cumulative_color)

    for project_id, project_data in projects_dict.items():
        axes.plot(indices, projects_weekly_total[project_id],
                  color=project_data['color'],
                  label=project_data['label'],
                  lw=3)

    # ~ additional plot info
    axes.set_title('Total weekly hours')
    axes.set_ylabel('time in hours')
    axes.set_ylim(0)
    axes.set_xticks(indices)
    axes.set_xticklabels([week[0].strftime(datetime_format) for week in weeks])
    axes.legend()

    axes_total.set_ylim(0, 50)
    axes_total.set_ylabel('cummulative time in hours', color='gray')
    axes_total.tick_params(labelcolor='gray')

    return axes
