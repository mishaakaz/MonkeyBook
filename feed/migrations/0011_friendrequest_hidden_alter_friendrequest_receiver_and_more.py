# Generated by Django 4.0 on 2022-01-13 13:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('feed', '0010_profile_surname_alter_like_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendrequest',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='friendrequest',
            name='receiver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='auth.user'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_of_birth',
            field=models.DateField(help_text='Дата рождения', null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(blank=True, help_text='Имя', max_length=64),
        ),
        migrations.AlterField(
            model_name='profile',
            name='nickname',
            field=models.CharField(help_text='Никнейм', max_length=32),
        ),
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, help_text='Фото профиля', null=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.CharField(blank=True, help_text='Статус', max_length=64),
        ),
        migrations.AlterField(
            model_name='profile',
            name='surname',
            field=models.CharField(blank=True, help_text='Фамилия', max_length=64),
        ),
    ]