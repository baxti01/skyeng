# Generated by Django 4.2.4 on 2023-08-27 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('code_review', '0004_logs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='period',
        ),
        migrations.RemoveField(
            model_name='file',
            name='start_datetime',
        ),
    ]
