# Generated by Django 4.1.7 on 2023-08-02 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('Sub_id', models.AutoField(primary_key=True, serialize=False)),
                ('Subject_Name', models.TextField(max_length=100)),
            ],
            options={
                'db_table': 'subject',
            },
        ),
    ]
