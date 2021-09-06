# Generated by Django 3.0.10 on 2021-09-01 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20210831_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jupyternotebook',
            name='title',
            field=models.CharField(help_text='The main title of the entry. Does not have to be unique', max_length=250),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(help_text='The main title of the entry. Does not have to be unique', max_length=250),
        ),
        migrations.AlterField(
            model_name='tutorial',
            name='title',
            field=models.CharField(help_text='The main title of the entry. Does not have to be unique', max_length=250),
        ),
    ]
