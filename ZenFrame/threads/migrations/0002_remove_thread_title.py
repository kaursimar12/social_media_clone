# Generated by Django 5.1.1 on 2024-09-29 21:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thread',
            name='title',
        ),
    ]
