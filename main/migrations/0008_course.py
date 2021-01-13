# Generated by Django 3.0.8 on 2021-01-13 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20210101_0545'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=50)),
                ('course_link', models.URLField(max_length=300)),
                ('description', models.TextField()),
                ('course_pic', models.ImageField(null=True, upload_to='images/course/')),
            ],
        ),
    ]
