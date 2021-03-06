# Generated by Django 4.0 on 2022-01-14 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('feed', '0012_profile_sex'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dialog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member1', to='auth.user')),
                ('member2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member2', to='auth.user')),
            ],
            options={
                'unique_together': {('member1', 'member2')},
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(help_text='Сообщение')),
                ('pub_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('is_readed', models.BooleanField(default=False)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
                ('chat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='feed.dialog')),
            ],
        ),
    ]
