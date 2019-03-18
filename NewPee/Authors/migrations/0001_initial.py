# Generated by Django 2.1.7 on 2019-03-17 20:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('displayName', models.CharField(max_length=15)),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('posts_created', models.PositiveIntegerField(default=0)),
                ('picture', models.URLField(blank=True)),
                ('github_url', models.URLField(blank=True)),
                ('followers', models.ManyToManyField(blank=True, related_name='_followers', to='Authors.Author')),
                ('following', models.ManyToManyField(blank=True, related_name='_following', to='Authors.Author')),
                ('friends', models.ManyToManyField(blank=True, related_name='_author_friends_+', to='Authors.Author')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
