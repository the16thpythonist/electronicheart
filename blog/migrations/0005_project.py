# Generated by Django 3.0.10 on 2021-08-28 18:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('blog', '0004_auto_20210306_1225'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('subtitle', models.CharField(blank=True, default='', max_length=250)),
                ('description', models.CharField(blank=True, default='', max_length=200)),
                ('slug', models.SlugField(default='auto', max_length=250, unique=True)),
                ('content', models.TextField(default='')),
                ('publishing_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('next', models.URLField(blank=True, null=True)),
                ('previous', models.URLField(blank=True, null=True)),
                ('author', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to=settings.AUTH_USER_MODEL)),
                ('thumbnail', filer.fields.image.FilerImageField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_thumbnail', to=settings.FILER_IMAGE_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
