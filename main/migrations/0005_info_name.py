# Generated by Django 3.0.8 on 2020-12-31 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20201230_0501'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='name',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
