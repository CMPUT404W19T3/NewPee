# Generated by Django 2.1.7 on 2019-03-21 06:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0002_auto_20190321_0619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='visibleTo',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]