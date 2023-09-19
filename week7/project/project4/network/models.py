from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.id} {self.username} {self.first_name} {self.last_name} {self.last_login} {self.date_joined} {self.email}"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Post Text")
    timeStamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}: {self.user} {self.text} {self.timeStamp}"
    
    @classmethod
    def create_post(cls, user, text):
        post = cls(user=user, text=text)
        post.save()
        return post
    
class Follower(models.Model):

    #The user following
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #The user beinng followed
    userfollow = models.IntegerField()
    dateFollowed = models.DateTimeField(auto_now_add=True)
    currentFollow = models.BooleanField()

    def __str__(self):
        return f"{self.id} {self.user} {self.userfollow} {self.dateFollowed} {self.currentFollow}"
    
    @classmethod
    def create_follow(cls, user, userfollow):
        follow = cls(user=user, userfollow=userfollow)
        follow.save()
        return follow