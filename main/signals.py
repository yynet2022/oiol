# -*- coding: utf-8 -*-
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from . import models


User = get_user_model()
Action = models.Action
Log = models.Log


@receiver(post_save, sender=User)
def create_user_post_save(sender, instance, created, **kwargs):
    if created:
        action = getattr(instance, 'action', None) or Action(user=instance)
        action.save()


@receiver(post_save, sender=Action)
def action_post_save(sender, instance, created, **kwargs):
    Log(user=instance.user, message=instance.getStat()).save()
