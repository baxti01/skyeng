# Generated by Django 4.2.4 on 2023-08-24 18:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('code_review', '0003_rename_task_date_file_start_datetime_file_period'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('linter', models.CharField(max_length=20)),
                ('sent_status', models.CharField(choices=[('sent', 'Sent'), ('not_sent', 'Not Sent')], default='not_sent')),
                ('log_text', models.TextField()),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='code_review.file')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
