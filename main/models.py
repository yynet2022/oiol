# -*- coding: utf-8 -*-
import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


User = get_user_model()
ACTION_OUT = 0
ACTION_IN = 1


class Action(models.Model):
    ACTION_CHOICES = (
        (ACTION_OUT, '退出'),
        (ACTION_IN,  '出社'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=0)
    action = models.IntegerField('勤務状態',
                                 default=ACTION_OUT, choices=ACTION_CHOICES)
    update_at = models.DateTimeField('更新日時', default=timezone.now)

    def isOut(self):
        return self.action == ACTION_OUT

    def isIn(self):
        return self.action == ACTION_IN

    def _setAction(self, v, by_myself=True):
        self.action = v
        self._by_myself = by_myself

    def setOut(self, by_myself=True):
        self._setAction(ACTION_OUT, by_myself)

    def setIn(self, by_myself=True):
        self._setAction(ACTION_IN, by_myself)

    def getStat(self):
        s = self.get_action_display()
        if not self._by_myself:
            s += "*"
        return s

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._by_myself = True

    def __str__(self):
        try:
            s = "<Action:%s," % self.user.get_full_name()
        except Exception:
            s = "<Action:-,"
        s += self.getStat() + ","
        s += str(timezone.localtime(self.update_at)) + ">"
        return s


class Log(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    create_at = models.DateTimeField('作成時刻', default=timezone.now)
    message = models.CharField('メッセージ', max_length=128)

    def __str__(self):
        try:
            u = self.user.get_full_name()
        except Exception:
            u = '-'
        return "Log<%s,%s,%s>" % (u, str(self.create_at), self.message)
