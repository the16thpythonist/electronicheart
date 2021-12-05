from django.contrib import admin

from .models import DailyStatistics


class DailyStatisticsAdmin(admin.ModelAdmin):

    # One thing to note here is that this list does not contain the "entry" field. This is because this is a generic
    # foreign key. These can apparently not be simply rendered (or even queried) as they are. This means when editing
    # a comment in the admin backend there is not simple way to just have dropdown menu to select which post to assign
    # this comment to. I think it would be possible, but it would be a bit more effort. For now a workaround is to have
    # the two fields 'content_type' and 'object_id' (Those actually make up the 'entry' field.
    fields = [
        'date',
        'hours_today',
        'hours_total',
        'daily_hours_plot',
        'weekly_hours_plot'
    ]
    # https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Admin_site
    # This is actually a sick functionality! As you can see with the name "get_shortened_content" is actually a method
    # but we can use the output of this method to fill a column in the list display! In this case the column contains
    # the first few characters of the content.
    list_display = ('date', 'hours_today')


admin.site.register(DailyStatistics, DailyStatisticsAdmin)

