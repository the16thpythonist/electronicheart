from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.forms import ModelForm
from django_summernote.admin import SummernoteModelAdmin

from .models import Tutorial


class TutorialAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(TutorialAdminForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = [
            'title',
            'subtitle',
            'slug',
            'content',
            'publishing_date',
            'creation_date',
            'next',
            'previous',
            'author'
        ]
        model = Tutorial


class TutorialAdmin(SummernoteModelAdmin):

    list_display = ('title', 'author', 'creation_date')

    summernote_fields = '__all__'
    form = TutorialAdminForm


admin.site.register(Tutorial, TutorialAdmin)
