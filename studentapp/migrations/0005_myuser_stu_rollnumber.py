# Generated by Django 4.1.7 on 2023-08-02 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentapp', '0004_myuser_last_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='stu_rollnumber',
            field=models.CharField(max_length=200, null=True),
        ),
    ]