# Generated by Django 4.2.3 on 2023-08-02 05:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studentapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='last_login',
        ),
    ]
