import random
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetDoneView

from django.contrib.auth.views import PasswordResetConfirmView

from django.contrib.auth.views import PasswordResetCompleteView
from Product.models import Category

# Create your views here.

def Home(request):
    return render(request, 'Home.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page or another page
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login_user')

    return render(request, 'login.html')

def reg_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login_user')  # Redirect to login page
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = UserCreationForm()

    return render(request, 'registration.html')


def logout_user(request):
    logout(request)
    messages.success(request, "User Logged Out.")  # Corrected to 'messages'
    return redirect('login_user')

def otp_verification(request):
    otp = random.randint(0000, 9999)
    subject = 'Your otp mail'
    message = (f'Hello please dont share your otp, your otp is {otp}')
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['mursalinpranto1342@gmail.com']
    send_mail(subject, message, from_email, recipient_list)
    return redirect('/')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        # Custom logic before sending the reset email
        messages.success(self.request, 'If an account exists with this email, you will receive a password reset email.')
        return super().form_valid(form)

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'
    success_url = reverse_lazy('login_user')
