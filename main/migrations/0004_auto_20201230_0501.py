# Generated by Django 3.0.8 on 2020-12-30 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_jobs'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='application_link',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='jobs',
            name='company_website',
            field=models.URLField(blank=True),
        ),
    ]
