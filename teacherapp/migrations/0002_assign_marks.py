# Generated by Django 4.1.7 on 2023-08-02 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacherapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assign_Marks',
            fields=[
                ('Sub_id', models.AutoField(primary_key=True, serialize=False)),
                ('Stu_Rollnum', models.TextField(max_length=100)),
                ('Sub_Name', models.TextField(max_length=100)),
                ('Sub_marks', models.TextField(max_length=100)),
                ('year', models.IntegerField()),
            ],
            options={
                'db_table': 'assign_marks',
            },
        ),
    ]
