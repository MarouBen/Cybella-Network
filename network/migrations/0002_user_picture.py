# Generated by Django 4.1.7 on 2023-03-24 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='network/images/profile_pictures'),
        ),
    ]
