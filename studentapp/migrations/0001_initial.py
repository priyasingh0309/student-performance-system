# Generated by Django 4.2.3 on 2023-08-01 14:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('stu_name', models.CharField(max_length=50, verbose_name='Name')),
                ('stu_contact', models.BigIntegerField(null=True)),
                ('stu_id', models.CharField(max_length=50)),
                ('stu_address', models.CharField(max_length=200)),
                ('stu_photo', models.FileField(upload_to='media')),
                ('datetime_created', models.DateTimeField(default=datetime.datetime.now)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'user_details',
            },
        ),
    ]
