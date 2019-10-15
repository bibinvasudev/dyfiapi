from mongoengine import Document
from mongoengine import FileField
from django.db import models


class CommonConfig(models.Model):
    name = models.CharField(max_length=50)
    banner_image = models.ImageField(upload_to='images/')


class Config(Document):
    banner_image = FileField()


