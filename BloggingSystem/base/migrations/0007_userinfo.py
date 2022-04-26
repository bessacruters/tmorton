# Generated by Django 4.0.3 on 2022-04-12 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_post_imagedate'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('websiteLink', models.CharField(max_length=200)),
                ('userName', models.CharField(max_length=50)),
            ],
        ),
    ]
