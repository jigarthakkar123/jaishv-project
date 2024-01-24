# Generated by Django 4.2.8 on 2024-01-09 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_user_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='profile',
        ),
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(default='', upload_to='profile_picture/'),
        ),
    ]
