# Generated by Django 5.1 on 2024-08-29 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Horrorify', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='liked_by',
        ),
        migrations.AddField(
            model_name='customuser',
            name='liked_stories',
            field=models.ManyToManyField(blank=True, related_name='liked_by_users', to='Horrorify.story'),
        ),
    ]
