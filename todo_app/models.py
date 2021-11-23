from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
# Create your models here.
from django_rest_passwordreset.signals import reset_password_token_created
from django_rest_passwordreset.views import User


class Task(models.Model):
    user = models.ForeignKey('auth.User', related_name='tasks', on_delete=models.CASCADE)
    title = models.TextField(null=True)
    description = models.TextField(null=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['created']


