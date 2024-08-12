from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    channelId = models.CharField("チャンネルID", max_length=255)
    msg = models.CharField("メッセージ", max_length=255)
    usr = models.CharField("ユーザ", max_length=255)
    start = models.DateField("開始")
    end = models.DateField("終了")