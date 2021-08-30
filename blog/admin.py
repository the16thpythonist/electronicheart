from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.forms import ModelForm
from django.contrib.contenttypes.admin import GenericTabularInline

from django_summernote.admin import SummernoteModelAdmin

from .models import Tutorial, Project
from .models import Comment

# Useful resources:
# https://docs.djangoproject.com/en/3.2/ref/contrib/admin/
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Admin_site


class TutorialAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(TutorialAdminForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = [
            'title',
            'subtitle',
            'description',
            'thumbnail',
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


class ProjectAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProjectAdminForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = [
            'title',
            'subtitle',
            'description',
            'thumbnail',
            'slug',
            'content',
            'publishing_date',
            'creation_date',
            'next',
            'previous',
            'author'
        ]
        model = Project


class ProjectAdmin(SummernoteModelAdmin):

    list_display = ('title', 'author', 'creation_date')

    summernote_fields = '__all__'
    form = ProjectAdminForm


class CommentAdmin(ModelAdmin):

    # One thing to note here is that this list does not contain the "entry" field. This is because this is a generic
    # foreign key. These can apparently not be simply rendered (or even queried) as they are. This means when editing
    # a comment in the admin backend there is not simple way to just have dropdown menu to select which post to assign
    # this comment to. I think it would be possible, but it would be a bit more effort. For now a workaround is to have
    # the two fields 'content_type' and 'object_id' (Those actually make up the 'entry' field.
    fields = [
        'name',
        'email',
        'hash_id',
        'image',
        'content',
        'publishing_date',
        'active',
        # 'entry' does not work!
        ('content_type', 'object_id')
    ]
    # https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Admin_site
    # This is actually a sick functionality! As you can see with the name "get_shortened_content" is actually a method
    # but we can use the output of this method to fill a column in the list display! In this case the column contains
    # the first few characters of the content.
    list_display = ('name', 'publishing_date', 'get_shortened_content')



admin.site.register(Tutorial, TutorialAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Comment, CommentAdmin)
