# Generated by Django 2.1.7 on 2019-04-08 22:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0005_auto_20190408_1629'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='post_date',
            new_name='published',
        ),
    ]
