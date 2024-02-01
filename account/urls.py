from django.urls import path
from . import views
from account.views import UserWcDataView, UserWcDeleteDataView, WheelchairUpdateAPIView, SendPasswordResetEmailView, UserChangePasswordView, UserLoginView, UserIdInfoView, UserSessionView, UserAllSessionView, UserIdSessionView, UserSensDataView, UserTimeStampSessionView, UserRegistrationView, UserPasswordResetView, UserSensorDataView, UserSessionDataView, home
urlpatterns = [
    path('create_user/', views.create_user, name='create_user'),
    path('register/', UserRegistrationView.as_view(), name='register'), #probably not using
    path('login/', UserLoginView.as_view(), name='login'),
    path('idinfo/', UserIdInfoView.as_view(), name='idinfo'),
    path('sessions/', UserSessionView.as_view(), name='sessions'),
    path('sensor-data/', UserSensorDataView.as_view(), name='sensor-data'),

    path('allsessions/', UserAllSessionView.as_view(), name='allsessions'),
    path('id-sessions/<int:id>/', UserIdSessionView.as_view(), name='id-sessions'),
    path('timestamp-sessions/<int:stt>/<int:ett>/', UserTimeStampSessionView.as_view(), name='timestamp-sessions'),
    path('sens-data/<int:id>/<int:stt>/<int:ett>/', UserSensDataView.as_view(), name='sens-data'),



    path('create_wheelchair/', views.create_wheelchair, name='create_wheelchair'),
    path('wcdata/', UserWcDataView.as_view(), name='wcdata'),
    path('wheelchair/<int:id>/',
         UserWcDeleteDataView.as_view(), name='UserWcDeleteDataView'),
    path('wheelchair-update/<int:id>/', WheelchairUpdateAPIView.as_view(), name='wheelchair-update'),

    path('check_access_token/', views.check_access_token, name='check_access_token'),
    path('refresh_access_token/', views.refresh_access_token, name='refresh_access_token'),

    path('session-data/', UserSessionDataView.as_view(), name='session-data'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    # path('passchange', home, name='home'),
]