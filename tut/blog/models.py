from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Account(models.Model):
    name = models.CharField(max_length=20)
    alert = models.BooleanField(default=False)
    registred_date = models.DateTimeField(default=timezone.now)
    started = models.BooleanField(default=False)

    def change_alert(self):
        self.alert = not self.alert

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    accounts = models.ForeignKey(Account, on_delete=models.CASCADE)

    def get_accounts(self):
        return self.accounts

    def __str__(self):
        return self.user.name


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
