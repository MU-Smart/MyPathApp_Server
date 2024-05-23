from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class SenData(models.Model):
    time_stamp = models.CharField(max_length=20)
    e = models.CharField(max_length=25)
    ax = models.CharField(max_length=20)
    ay = models.CharField(max_length=20)
    az = models.CharField(max_length=20)
    gx = models.CharField(max_length=20)
    gy = models.CharField(max_length=20)
    gz = models.CharField(max_length=20)
    mx = models.CharField(max_length=20)
    my = models.CharField(max_length=20)
    mz = models.CharField(max_length=20)
    lat = models.CharField(max_length=20)
    lng = models.CharField(max_length=20)
    p = models.CharField(max_length=20)
    s = models.CharField(max_length=20)

    def __str__(self):
        return self.t


class SessionData(models.Model):
    uid = models.IntegerField()
    st = models.CharField(max_length=25)
    et = models.CharField(max_length=20)
    sbt = models.IntegerField()
    wcId = models.CharField(max_length=20)
    sq1 = models.CharField(max_length=20)
    sq2 = models.CharField(max_length=20)
    sq3 = models.CharField(max_length=20)
    eq1 = models.CharField(max_length=20)
    eq2 = models.CharField(max_length=20)
    v = models.CharField(max_length=25, default="old")

    def __str__(self):
        return self.t


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, name, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    com_num = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Ensure this field is present
    tc = models.BooleanField(default=True)  # Add this line
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)  # Add this field if not present

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    height = models.CharField(max_length=20, blank=True)
    weight = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    age = models.CharField(max_length=20, null=True, blank=True)

class Wheelchair(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    type_wc = models.CharField(max_length=20, blank=True)
    wc_identify = models.CharField(max_length=20)
    number_w = models.IntegerField(null=True, blank=True)
    d_type = models.CharField(max_length=20, blank=True)
    tire_mat = models.CharField(max_length=20, blank = True)
    wc_wdt = models.IntegerField(null=True, blank=True)
    wc_ht = models.IntegerField(null=True, blank=True)
