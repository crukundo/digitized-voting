# Generated by Django 3.1 on 2021-04-27 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institution', '0004_merge_20210427_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='mugshot',
            field=models.ImageField(blank=True, null=True, upload_to='candidates/'),
        ),
    ]
