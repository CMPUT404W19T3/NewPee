# Generated by Django 2.1.7 on 2019-03-25 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authors', '0002_auto_20190324_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='host',
            field=models.URLField(default='newpee.herokuapp.com/'),
        ),
    ]
