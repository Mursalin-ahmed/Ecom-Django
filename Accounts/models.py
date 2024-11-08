from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/', null=True, blank=True, default='default.jpg')
    otp = models.CharField(max_length=6, validators=[MinLengthValidator(6)], null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'



