# Generated by Django 4.0.3 on 2022-04-12 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='imageDate',
            field=models.DateTimeField(),
        ),
    ]