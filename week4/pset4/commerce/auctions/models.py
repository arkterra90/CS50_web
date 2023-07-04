from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass

class Listing(models.Model):

    conditions = [
    ("New", "New"),
    ("Used", "Used")
] 
    title = models.CharField(max_length=64)
    discription = models.TextField()
    condition = models.CharField(choices=conditions, default="")

class bids(models.Model):
    pass

class comments(models.Model):
    pass