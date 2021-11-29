"""This module is used to create the models in database"""
from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django_rest_passwordreset.signals import reset_password_token_created


# Create your models here.

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):  # pylint: disable=W0613
    """
    Massage reset token to command line
    :param sender: None
    :param instance: None
    :param reset_password_token: Rest Token
    :param args: None
    :param kwargs: None
    :return:
        Send rest password token to command line
    """

    email_plaintext_message = "{}?token={}, {}, {}, {}, {}".format(
        reverse('password_reset:reset-password-request'),
        reset_password_token.key,
        sender,
        instance,
        args,
        kwargs
    )

    send_mail(
        # title:
        "Password Reset for TODO APP",
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )


class Task(models.Model):
    """This class is used to create task table in database"""
    task_title = models.CharField(max_length=200, blank=False)
    task_description = models.TextField(blank=True)
    is_complete = models.BooleanField(blank=False, default=False)

    category = [
        ("Home Task", "Home Task"),
        ("Office Task", "Office Task"),
        ("MISC", 'Miscellaneous')
    ]

    task_category = models.CharField(max_length=20, choices=category, blank=False)
    task_start_date = models.DateTimeField(auto_now=True)
    task_end_date = models.DateTimeField(blank=True, null=True)
    person = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        """
        String representation of class
        :return: Task Title
        """
        return str(self.task_title)

    class Meta:  # pylint: disable=R0903
        """
        Specifying Task Order
        """
        ordering = ['pk']