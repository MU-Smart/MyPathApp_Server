from rest_framework import serializers
from account.models import User, SenData, SessionData
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import Util


from rest_framework import serializers
from .models import User, Profile, Wheelchair



class WheelchairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wheelchair
        fields = ('type_wc', 'wc_identify', 'number_w',
                  'd_type', 'tire_mat', 'wc_wdt', 'wc_ht')

    # def validate(self, attrs):
    #   userid = attrs.get('user_id')
    #   user = User.objects.get(id=userid)


    #   return attrs


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('height', 'weight', 'gender', 'age')

class UserRegistrationSerializer(serializers.ModelSerializer):
    # Nested serializer for Profile and Wheelchair model
    profile = ProfileSerializer(required=True)
    wheelchair = WheelchairSerializer(required=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'name', 'com_num', 'is_active', 'is_admin', 'profile', 'wheelchair')
        extra_kwargs = {
            'is_active': {'read_only': True},
            'is_admin': {'read_only': False},
        }

    def create(self, validated_data):
      try:
        profile_data = validated_data.pop('profile')
        wheelchair_data = validated_data.get('wheelchair')
        password = validated_data.pop('password')
        user_instance = User.objects.create(**validated_data)
        user_instance.set_password(password)
        Profile.objects.create(user=user_instance, **profile_data)
        Wheelchair.objects.create(user=user_instance, **wheelchair_data)
        user_instance.save()
        return user_instance
      except Exception as e:
        print("==== Exception raised in serializer ====")
        print(e)

class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password']

class UserSensorDataSerializer(serializers.ModelSerializer):
  class Meta:
    model = SenData
    fields = ['time_stamp', 'e', 'ax', 'ay', 'az', 'gx', 'gy', 'gz', 'mx', 'my', 'mz', 'lat', 'lng', 'p', 's']

class UserSessionDataSerializer(serializers.ModelSerializer):
  class Meta:
    model = SessionData
    fields = ['uid', 'st', 'et', 'sbt', 'wcId', 'sq1', 'sq2', 'sq3', 'eq1', 'eq2', 'v']


class UserIdInfoSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'name']

class UserSessionSerializer(serializers.ModelSerializer):
  class Meta:
    model = SessionData
    fields = ['uid', 'st', 'et', 'sbt', 'pp', 'v']

class UserChangePasswordSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    user = self.context.get('user')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    user.set_password(password)
    user.save()
    return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    fields = ['email']

  def validate(self, attrs):
    email = attrs.get('email')
    if User.objects.filter(email=email).exists():
      user = User.objects.get(email = email)
      uid = urlsafe_base64_encode(force_bytes(user.id))
      print('Encoded UID', uid)
      token = PasswordResetTokenGenerator().make_token(user)
      print('Password Reset Token', token)
      link = 'http://127.0.0.1:8080/?token='+uid+'/'+token
      print('Password Reset Link', link)

      # Send EMail
      body = 'Click Following Link to Reset Your Password '+link
      data = {
        'subject':'Reset Your Password',
        'body':body,
        'to_email':user.email
      }
      Util.send_email(data)
      return attrs
    else:
      raise serializers.ValidationError('You are not a Registered User')

class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      password2 = attrs.get('password2')
      uid = self.context.get('uid')
      token = self.context.get('token')
      if password != password2:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      id = smart_str(urlsafe_base64_decode(uid))
      user = User.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')
  