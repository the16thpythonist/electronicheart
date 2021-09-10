# Generated by Django 3.0.10 on 2021-08-31 12:15

from django.conf import settings
from django.db import migrations
import django.db.models.deletion
import filer.fields.file
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.FILER_IMAGE_MODEL),
        ('filer', '0012_file_mime_type'),
        ('blog', '0013_jupyternotebook'),
    ]

    operations = [
        migrations.AddField(
            model_name='jupyternotebook',
            name='thumbnail',
            field=filer.fields.image.FilerImageField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jupyter_thumbnail', to=settings.FILER_IMAGE_MODEL),
        ),
        migrations.AlterField(
            model_name='jupyternotebook',
            name='jupyter_file',
            field=filer.fields.file.FilerFileField(on_delete=django.db.models.deletion.CASCADE, related_name='jupyter_file', to='filer.File'),
        ),
    ]