# Generated by Django 4.1.7 on 2023-04-22 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0013_comment_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='comments',
            field=models.ManyToManyField(blank=True, related_name='comments', to='network.post'),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
