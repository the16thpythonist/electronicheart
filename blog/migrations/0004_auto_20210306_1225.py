# Generated by Django 3.0.10 on 2021-03-06 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20210306_1156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorial',
            name='slug',
            field=models.SlugField(default='auto', max_length=250, unique=True),
        ),
    ]
