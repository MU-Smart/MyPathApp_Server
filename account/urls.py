from django.urls import path
from account.views import SendPasswordResetEmailView, UserChangePasswordView, UserLoginView, UserProfileView, UserSessionView, UserRegistrationView, UserPasswordResetView, UserSensorDataView, UserSessionDataView, home
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('sessions/', UserSessionView.as_view(), name='sessions'),
    path('sensor-data/', UserSensorDataView.as_view(), name='sensor-data'),
    path('session-data/', UserSessionDataView.as_view(), name='session-data'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    # path('passchange', home, name='home'),
]