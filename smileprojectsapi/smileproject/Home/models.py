from django.db import models
from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
# from django.contrib.auth.models import BaseUserManager


# user = BaseUserManager
class User(AbstractUser):
    gender = (
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE'),
    )
    age = (
        ('18_24', '18-24'),
        ('25-34', '25-34'),
        ('35-44', '35-44'),
        ('45-54', '45-54'),
        ('55-64', '55-64'),
        ('64 AND OLDER', '64 AND OLDER'),
    )
    relationship = (
        ('YES', 'YES'),
        ('NO', 'NO'),
    )
    children = (
        ('YES', 'YES'),
        ('NO', 'NO'),
    )
    goal = (
        ("I want to increase happiness", "I want to increase happiness"),
        ("I want to express gratitude", "I want to express gratitude"),
        ("I want an energy boost", "I want an energy boost"),
        ("I want to feel more confident", "I want to feel more confident"),
        ("I wanat to feel peace", "I wanat to feel peace")
    )
    email = models.EmailField(_('email'), blank=True, unique=True,null=True)
    NAME = models.CharField(max_length=30, null=True, blank=True)
    GENDER = models.CharField(max_length=30, choices=gender, null=True, blank=True)
    AGE = models.CharField(max_length=30, choices=age, null=True, blank=True)
    RELATIONSHIP = models.CharField(max_length=30, choices=relationship, blank=True, null=True)
    CHILDREN = models.CharField(max_length=30, choices=children, blank=True, null=True)
    GOAL = MultiSelectField(choices=goal, null=True, blank=True)




class DailyQuote(models.Model):
    CONTENT = models.TextField()
    DATE = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.DATE)


class Smile(models.Model):
    user = models.ForeignKey(User, related_name='smile_user', on_delete=models.CASCADE)
    smileSecond = models.IntegerField()
    DATE = models.DateField()

    def __str__(self):
        return str(self.DATE)


class Goal(models.Model):
    user = models.ForeignKey(User, related_name='smile_user1', on_delete=models.CASCADE)
    smile_count = models.IntegerField()
    smile_second = models.IntegerField()

    def __str__(self):
        return str(self.user)


class Activity(models.Model):
    title = models.CharField(max_length=40)
    img = models.ImageField(upload_to="media")
    description = models.TextField()
    createdate = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.title)


class Favourite(models.Model):
    user = models.ForeignKey(User, related_name='favourite_user', on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, models.CASCADE, related_name='activity')

    def __str__(self):
        return str(self.id)


class Community(models.Model):
    tilte = models.CharField(max_length=30)
    img = models.ImageField(upload_to="media")
    description = models.TextField()

    def __str__(self):
        return str(self.tilte)


class Smilescience(models.Model):
    tilte = models.CharField(max_length=30)
    img = models.ImageField(upload_to="media")
    description = models.TextField()

    def __str__(self):
        return str(self.tilte)


class Resource(models.Model):
    choice = (
        ('COMMUNITY', 'COMMUNITY'),
        ('SMILE SCIENCE', 'SMILE SCIENCE'),
        ('LEVEL', 'LEVEL'),
        ('NOTIFICATION', 'NOTIFICATION'),
    )
    name = models.CharField(max_length=30)
    resource = models.CharField(max_length=30, choices=choice)
    img = models.ImageField(upload_to="media")

    def __str__(self):
        return str(self.name)




@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    context = {
        'username': reset_password_token.user.get_full_name(),
        'reset_password_token': reset_password_token.key
    }

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), context)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )