from django.db import models
from datetime import datetime
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    stu_name = models.CharField(verbose_name='Name', max_length=50)
    stu_contact = models.BigIntegerField(null=True)
    stu_id = models.CharField(max_length=50)
    stu_address = models.CharField(max_length=200)
    stu_rollnumber = models.CharField(max_length=200, null=True)
    stu_status = models.CharField(max_length=50, default = 'pending', null = True)
    stu_performance = models.CharField(max_length = 2, null = True)
    stu_photo = models.FileField(upload_to='media')
    datetime_created = models.DateTimeField(default=datetime.now)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["date_of_birth"]

    def _str_(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    class Meta:
        db_table = 'user_details'

class Profile(models.Model):
    stu_foregin = models.OneToOneField(MyUser,on_delete=models.CASCADE)
    forget_token = models.CharField(max_length=1000)
    class Meta:
        db_table = 'Forget_password'

class Feeback(models.Model):
    Feed_id = models.AutoField(primary_key = True)
    Stu_Foregin = models.ForeignKey(MyUser, on_delete = models.CASCADE)
    Rating = models.IntegerField()
    Review = models.TextField(max_length = 500)
    Sentiment = models.TextField(max_length = 500, null=True)

    class Meta:
        db_table = 'feedback_details'