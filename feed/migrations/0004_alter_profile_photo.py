# Generated by Django 4.0 on 2022-01-04 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0003_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]