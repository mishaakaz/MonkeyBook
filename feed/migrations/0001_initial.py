# Generated by Django 3.2.9 on 2021-12-11 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Введите имя', max_length=64)),
                ('nickname', models.CharField(help_text='Введите никнейм', max_length=32)),
                ('date_of_birth', models.DateField(help_text='Укажите дату рождения', null=True)),
                ('status', models.CharField(blank=True, help_text='Введите статус', max_length=64)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='userImages/')),
            ],
        ),
    ]
