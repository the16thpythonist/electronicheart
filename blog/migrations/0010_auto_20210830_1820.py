# Generated by Django 3.0.10 on 2021-08-30 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20210830_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='hash_id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
