# Generated by Django 4.1.7 on 2023-04-21 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0010_post_repost'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bookmarks',
            field=models.ManyToManyField(blank=True, related_name='bookmarked_by', to='network.post'),
        ),
    ]
