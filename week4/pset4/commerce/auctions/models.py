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

    title = models.CharField(verbose_name='Listing Title', max_length=64)
    discription = models.TextField(verbose_name='Listing Discription')
    category = models.CharField(max_length=9, choices=categories, default="")
    bid_start = models.DecimalField(verbose_name='Starting Bid', max_digits=10, decimal_places=2, default='0.00')
    list_user = models.CharField(verbose_name='Listing User', max_length=64, null=True, blank=True)
    list_time = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(null=True, blank=True)
    def __str__(self):
        return f"{self.id}: {self.title} {self.discription} {self.category} {self.list_user} {self.image_url}"

class bids(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=10, decimal_places=2)
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