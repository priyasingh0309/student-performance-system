from django.db import models
from studentapp.models import MyUser
# Create your models here.

class Subject(models.Model):
    Sub_id = models.AutoField(primary_key=True)
    Subject_Name = models.TextField(max_length=100)

    class Meta:
        db_table = 'subject'

class Assign_Marks(models.Model):
    Sub_id = models.AutoField(primary_key=True)
    Stu_foregin = models.ForeignKey(MyUser, on_delete = models.CASCADE, null = True)
    Stu_Rollnum = models.TextField(max_length=100)
    Sub_Name = models.TextField(max_length=100)
    Sub_marks = models.TextField(max_length=100)
    Sub_Grade = models.TextField(max_length = 5, null = True)
    year = models.IntegerField()

    class Meta:
        db_table = 'assign_marks'

class Upload_Dataset(models.Model):
    UD_id = models.AutoField(primary_key=True)
    Upload_Dataset = models.FileField(upload_to = 'dataset')

    class Meta:
        db_table = 'upload_dataset'