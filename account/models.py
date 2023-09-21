from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser


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
    pp = models.CharField(max_length=25, default="-1")
    v = models.CharField(max_length=25, default="old")

    def __str__(self):
        return self.t

#  Custom User Manager
class UserManager(BaseUserManager):
  def create_user(self, email, name, tc, height, weight, gender, age, type_wc, number_w, wheel_type, tire_mat, wc_wdt, wc_ht, password=None, password2=None):
      """
      Creates and saves a User with the given email, name, tc and password.
      """
      if not email:
          raise ValueError('User must have an email address')

      user = self.model(
          email=self.normalize_email(email),
          name=name,
          tc=tc,
          height=height, 
          weight=weight,
          gender=gender,
          age=age,
          type_wc=type_wc,
          number_w=number_w,
          wheel_type=wheel_type,
          tire_mat=tire_mat,
          wc_wdt=wc_wdt,
          wc_ht=wc_ht,
      )

      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email, name, tc, height, weight, gender, age, type_wc, number_w, wheel_type, tire_mat, wc_wdt, wc_ht, password=None):
      """
      Creates and saves a superuser with the given email, name, tc and password.
      """
      user = self.create_user(
          email,
          password=password,
          name=name,
          tc=tc,
          height=height, 
          weight=weight,
          gender=gender,
          age=age,
          type_wc=type_wc,
          number_w=number_w,
          wheel_type=wheel_type,
          tire_mat=tire_mat,
          wc_wdt=wc_wdt,
          wc_ht=wc_ht,
      )
      user.is_admin = True
      user.save(using=self._db)
      return user


#  Custom User Model
class User(AbstractBaseUser):
  email = models.EmailField(
      verbose_name='Email',
      max_length=255,
      unique=True,
  )
  name = models.CharField(max_length=200)
  tc = models.BooleanField()
  height = models.CharField(max_length=20)
  weight = models.CharField(max_length=20)
  gender = models.CharField(max_length=20)
  age = models.CharField(max_length=20)
  type_wc = models.CharField(max_length=20)
  number_w = models.CharField(max_length=20)
  wheel_type = models.CharField(max_length=20)
  tire_mat = models.CharField(max_length=20)
  wc_wdt = models.CharField(max_length=20)
  wc_ht = models.CharField(max_length=20)
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name', 'tc']

  def __str__(self):
      return self.email

  def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return self.is_admin

  def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True

  @property
  def is_staff(self):
      "Is the user a member of staff?"
      # Simplest possible answer: All admins are staff
      return self.is_admin


