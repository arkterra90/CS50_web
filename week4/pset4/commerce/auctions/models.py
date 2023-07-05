from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass

class Listing(models.Model):

    conditions = [
    ("New", "New"),
    ("Used", "Used")
] 
    
    categories = [
        ("Home", "Home"),
        ("Tech", "Tech"),
        ("Tools", "Tools"),
        ("Toys", "Toys")
    ]

    title = models.CharField(max_length=64)
    discription = models.TextField()
    condition = models.CharField(max_length=5, choices=conditions, default="")
    category = models.CharField(max_length=9, choices=categories, default="")
    list_user = models.IntegerField()
    list_time = models.DateTimeField(auto_now_add=True)
    list_pic = models.ImageField(upload_to='images/')

    def __str__(self):
        return f"{self.id}: {self.title} {self.discription} {self.condition} {self.category} {self.list_user}"

class bids(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid = models.IntegerField()
    bid_time = models.DateTimeField(auto_now_add=True)
    bid_user = models.IntegerField()

    def __str__(self):
        return f"{self.id}: {self.item} {self.bid} {self.bid_time} {self.bid_user}"
    

class comments(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)
    item_comment = models.TextField()
    user_comment = models.IntegerField()
    time_comment = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self:id}: {self.item} {self.item_comment} {self.user_comment} {self.time_comment}"