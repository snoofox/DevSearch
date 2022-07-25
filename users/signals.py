from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings


@receiver(post_save, sender=User)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )
        subject = "Welcome to DevSearch!"
        message = "We're glad to have you."

        send_mail(
            subject, message, settings.DEFAULT_FROM_EMAIL, [profile.email]
        )


@receiver(post_save, sender=Profile)
def updateUser(sender, instance, created, **kwargs):
    user = instance.user
    if created:
        user.first_name = instance.name
        user.username = instance.username
        user.email = instance.email
        user.save()


@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass
