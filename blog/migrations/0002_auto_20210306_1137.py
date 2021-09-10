# Generated by Django 3.0.10 on 2021-03-06 11:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutorial',
            name='description',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='tutorial',
            name='thumbnail',
            field=filer.fields.image.FilerImageField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tutorial_thumbnail', to=settings.FILER_IMAGE_MODEL),
        ),
    ]