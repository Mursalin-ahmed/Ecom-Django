from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
from .views import CustomPasswordResetView

urlpatterns = [
    path('', Home, name='home'),
    path('login_user/', login_user, name='login_user'),
    path('reg_user/', reg_user, name= 'reg_user'),
    path('logout/', logout_user, name='logout'),
    path('otp_verification/', otp_verification, name= 'otp_verification'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

