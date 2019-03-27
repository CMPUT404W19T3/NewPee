
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='friend_requests',
            field=models.ManyToManyField(blank=True, related_name='_friend_requests', to='Authors.Author'),
        ),
    ]
