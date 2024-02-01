from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import WheelchairSerializer, SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserIdInfoSerializer, UserSessionSerializer, UserRegistrationSerializer, UserSensorDataSerializer, UserSessionDataSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from account.models import SessionData
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime
from django.http import JsonResponse
import os
from rest_framework.decorators import api_view
from .models import User, Wheelchair, SenData
from django.shortcuts import render
from rest_framework import generics
import json


def home(request):
    return os.path.join(request, 'home.html')

# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }


@api_view(['POST'])
def create_user(request):
    print(request.data)
    try:
      if request.method == 'POST':
          user_serializer = UserRegistrationSerializer(data=request.data)
          if user_serializer.is_valid():
              user_instance = user_serializer.save()
              return Response(user_serializer.data, status=status.HTTP_201_CREATED)
          else:
            print("User is not valid")

          return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
      print(e)

@api_view(['POST'])
def create_wheelchair(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid author ID'}, status=400)
        wheelchair = Wheelchair(
            type_wc=data['type_wc'], wc_identify=data['wc_identify'], number_w=data['number_w'], d_type=data['d_type'], tire_mat=data['tire_mat'], wc_wdt=data['wc_wdt'], wc_ht=data['wc_ht'],  user=user)
        wheelchair.save()
        return JsonResponse({'success': 'Wheelchair created successfully'}, status=201)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


class UserWcDataView(APIView):
  print("==============================================")
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]

  def get(self, request, format=None):
   try:
       serializer = UserIdInfoSerializer(request.user)
       data = Wheelchair.objects.filter(
           user_id=serializer.data['id']).values('id', 'type_wc', 'wc_identify', 'number_w', 'd_type', 'tire_mat', 'wc_wdt', 'wc_ht')
       return JsonResponse(list(data), safe=False, status=status.HTTP_200_OK)
   except Exception as err:
       print("Error {}".format(err))

class WheelchairUpdateAPIView(generics.UpdateAPIView):
  queryset = Wheelchair.objects.all()
  serializer_class = WheelchairSerializer
  lookup_field = 'id'  # This specifies the field used for looking up the object

  def perform_update(self, serializer):
    try:
      serializer.save()
      return JsonResponse("Wleelchair is updated", safe=False, status=status.HTTP_200_OK)
    except Exception as err:
      print("Error {}".format(err))
class UserWcDeleteDataView(APIView):
  print("===================Delete wheelchair===========================")
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]

  def delete(self, request, id, format=None):
    try:
      print("===================Delete wheelchair===========================")
      print(id)
      try:
        instance = Wheelchair.objects.get(id = id)
        instance.delete()
        return JsonResponse(
            {'success': 'Wheelchair deleted successfully'}, status=201)
      except Exception as err:
        print("Erro {}".format(err))
       #data = Wheelchair.objects.filter(
       #user_id=serializer.data['id']).values('type_wc', 'wc_identify', 'number_w')
       #return JsonResponse(list(data), safe=False, status=status.HTTP_200_OK)
    except Exception as err:
       return JsonResponse(
           {'success': 'This wheelchair is not available'}, status=status.HTTP_404_NOT_FOUND)
    
    return JsonResponse(
        {'error': 'This wheelchair is not available'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def check_access_token(request):
    access_token = request.data.get('access_token')
    if access_token:
        try:
            # Validate the access token
            token = AccessToken(access_token)
            expiration_timestamp = token['exp']
            expiration_datetime = datetime.utcfromtimestamp(expiration_timestamp)
            expiration_datetime = timezone.make_aware(expiration_datetime, timezone.utc)

            if expiration_datetime > timezone.now():
                # Access token is valid and not expired
                return Response({'status': 'active'}, status=status.HTTP_200_OK)
            else:
                # Access token has expired
                return Response({'status': 'expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            # Access token is invalid
            print(e)
            print("EXCEPTION")
            return Response({'status': 'invalid'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        # No access token provided in the request
        return Response({'status': 'missing'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def refresh_access_token(request):
  print("refresh_token")
  print(request.data)
  refresh_token = request.data.get('refresh_token')
  if refresh_token:
      try:
          refresh_token = RefreshToken(refresh_token)
          new_access_token = str(refresh_token.access_token)
          return Response({'access_token': new_access_token}, status=status.HTTP_200_OK)
      except Exception as e:
          return Response({'error': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)
  else:
      return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = get_tokens_for_user(user)
    return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserSensorDataView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    #print(request.data)
    serializer = UserSensorDataSerializer(data=request.data, many=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({'msg':'Data sent successfully'}, status=status.HTTP_200_OK)

class UserSessionDataView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    print(request.data)
    serializer = UserSessionDataSerializer(data=request.data, many=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({'msg':'Session data sent!'}, status=status.HTTP_200_OK)


class UserIdInfoView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    print("--------------------------")
    serializer = UserIdInfoSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

class UserSessionView(APIView):
  print("==============================================")
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
   try:
        serializer = UserIdInfoSerializer(request.user)
        data = SessionData.objects.filter(uid=serializer.data['id']).values('st', 'et', 'sbt')
        return JsonResponse(list(data), safe=False, status=status.HTTP_200_OK)
   except Exception as err:
        print("Erro {}".format(err))
  # data = MyModel.objects.all().values('field1', 'field2')
  # return JsonResponse(list(data), safe=False)
  # def get(self, request, format=None):
  #   serializer = UserSessionSerializer(uid=8)
  #   return Response(serializer.data, status=status.HTTP_200_OK)

class UserAllSessionView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
   try:
        data = SessionData.objects.all().values()
        return JsonResponse(list(data), safe=False, status=status.HTTP_200_OK)
   except Exception as err:
        print("Erro {}".format(err))

class UserIdSessionView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, id, format=None):
    try:
        # want to retrieve data from the SessionData table
        data = SessionData.objects.filter(uid=id).values()

        return JsonResponse(list(data), safe=False, status=status.HTTP_200_OK)
    except Exception as err:
        print("Error {}".format(err))

class UserTimeStampSessionView(APIView):
  print("=============")
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, stt, ett, format=None):
    try:

        # want to retrieve data from the SessionData table
        print(stt)
        print(ett)
        data = SessionData.objects.filter(st__gt=stt, et__lt=ett).values()

        return JsonResponse(list(data), safe=False, status=status.HTTP_200_OK)
    except Exception as err:
        print("Error {}".format(err))

class UserSensDataView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, id, stt, ett, format=None):
    try:
        # want to retrieve data from the SessionData table
        data = SenData.objects.filter(e=id, time_stamp__gt=stt, time_stamp__lt=ett ).values()
        return JsonResponse(list(data), safe=False, status=status.HTTP_200_OK)
    except Exception as err:
        print("Error {}".format(err))

class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)


