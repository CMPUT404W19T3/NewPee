# Generated by Django 2.1.7 on 2019-03-29 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Servers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='isActive',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='server',
            name='password',
            field=models.CharField(default='test_pass', max_length=140),
        ),
        migrations.AddField(
            model_name='server',
            name='username',
            field=models.CharField(default='testuser', max_length=140),
        ),
    ]
