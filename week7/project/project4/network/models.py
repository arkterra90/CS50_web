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
    likeCount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.id}: {self.user} {self.text} {self.timeStamp} {self.likeCount}"
    
    @classmethod
    def create_post(cls, user, text):
        post = cls(user=user, text=text)
        post.save()
        return post
    
class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.IntegerField()
    currentLike = models.BooleanField()
    likeDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post} {self.user} {self.currentLike} {self.likeDate}"
    
    @classmethod
    def create_PostLike(cls, post, user, currentLike):
        PostLike = cls(post=post, user=user, currentLike=currentLike)
        PostLike.save()
        return PostLike


class Follower(models.Model):

    #The user following
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #The user being followed
    userfollow = models.IntegerField()
    dateFollowed = models.DateTimeField(auto_now_add=True)
    currentFollow = models.BooleanField()

    def __str__(self):
        return f"{self.id} {self.user} {self.userfollow} {self.dateFollowed} {self.currentFollow}"
    
    @classmethod
    def create_follow(cls, user, userfollow, currentFollow):
        follow = cls(user=user, userfollow=userfollow, currentFollow=currentFollow)
        follow.save()
        return follow