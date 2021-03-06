# Generated by Django 2.1.7 on 2019-04-03 07:21

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
                ('url', models.URLField(blank=True, null=True)),
                ('host', models.URLField(default='newpee.herokuapp.com/')),
                ('displayName', models.CharField(max_length=15)),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('posts_created', models.PositiveIntegerField(default=0)),
                ('image', models.ImageField(blank=True, upload_to='profile_image', default='NewPee.png')),
                ('github_url', models.URLField(blank=True)),
                ('isAuthorized', models.BooleanField(default=True)),
                ('followers', models.ManyToManyField(blank=True, related_name='_followers', to='Authors.Author')),
                ('following', models.ManyToManyField(blank=True, related_name='_following', to='Authors.Author')),
                ('friend_requests', models.ManyToManyField(blank=True, related_name='_friend_requests', to='Authors.Author')),
                ('friends', models.ManyToManyField(blank=True, related_name='_author_friends_+', to='Authors.Author')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ForeignAuthor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('url', models.URLField(blank=True, max_length=1000, null=True)),
                ('host', models.URLField(default='newpee.herokuapp.com/')),
                ('displayName', models.CharField(max_length=15)),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('posts_created', models.PositiveIntegerField(default=0)),
                ('picture', models.URLField(blank=True)),
                ('github_url', models.URLField(blank=True)),
                ('isAuthorized', models.BooleanField(default=True)),
                ('followers', models.ManyToManyField(blank=True, related_name='_followersForeign', to='Authors.Author')),
                ('following', models.ManyToManyField(blank=True, related_name='_followingForeign', to='Authors.Author')),
                ('friend_requests', models.ManyToManyField(blank=True, related_name='_friend_requestsForeign', to='Authors.Author')),
                ('friends', models.ManyToManyField(blank=True, related_name='_friendsForeign', to='Authors.Author')),
            ],
        ),
    ]
