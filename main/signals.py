# -*- coding: utf-8 -*-
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from . import models


User = get_user_model()
Action = models.Action


@receiver(post_save, sender=User)
def create_user_post_save(sender, user, created, **kwargs):
    if created:
        action = getattr(user, 'action', None) or Action(user=user)
        action.save()
