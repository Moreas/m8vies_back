# Generated by Django 3.1.6 on 2021-06-25 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20210625_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='trailer_key',
            field=models.CharField(max_length=50, null=True),
        ),
    ]