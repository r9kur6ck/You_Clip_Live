from django.db import models
from django.contrib.auth.models import User

class Clip(models.Model):
    start = models.CharField("開始", max_length=255)
    end = models.CharField("終了", max_length=255)