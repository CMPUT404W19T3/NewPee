# Generated by Django 2.1.7 on 2019-03-25 16:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Authors', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('author', models.CharField(max_length=140)),
                ('content', models.CharField(max_length=140)),
                ('post_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='media/')),
                ('viewers', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=30)),
                ('source', models.URLField(blank=True, null=True)),
                ('origin', models.URLField(blank=True, null=True)),
                ('description', models.CharField(default='No Description', max_length=150)),
                ('content_type', models.TextField(default='text/plain')),
                ('content', models.TextField()),
                ('image', models.URLField(blank=True, null=True)),
                ('post_date', models.DateTimeField(auto_now_add=True)),
                ('visibility', models.CharField(choices=[('PUBLIC', 'PUBLIC'), ('FOAF', 'FOAF'), ('PRIVATE', 'PRIVATE'), ('SERVERONLY', 'SERVERONLY'), ('FRIENDS', 'FRIENDS')], default='PUBLIC', max_length=10)),
                ('unlisted', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Posts.Post')),
                ('visibleTo', models.ManyToManyField(blank=True, to='Authors.Author')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Posts.Post'),
        ),
    ]
