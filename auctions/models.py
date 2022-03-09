from asyncio.windows_events import NULL
from email.policy import default
from tkinter import CASCADE
from turtle import mode
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

def get_default_user():
    return User.objects.get(id=1)

class Listing(models.Model):
    title =models.CharField(max_length=64)
    category=models.CharField(max_length=64,default="household")
    description = models.CharField(max_length=64, default="")
    image_url=models.URLField(blank=True)
    price=models.FloatField(max_length=64,default=0)
    created_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name="creator",default=1)
    won_by=models.CharField(max_length=64, default="",blank=True)
    status=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    amount=models.FloatField(max_length=64)
    listing=models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="bids")
    bid_by=models.CharField(max_length=64,default="None")
    def __str__(self):
        return f"{self.amount}"

class Watchlist(models.Model):
    watchlist=models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="list")
    added_by=models.ForeignKey(User,on_delete=models.CASCADE,related_name="adder")

    def __str__(self):
        return f"{self.added_by}"

class Comment(models.Model):
    comment_desc=models.CharField(max_length=300)
    commented_on=models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="commented_on")
    commentor=models.CharField(max_length=64,default="None")

    def __str__(self):
        return f"{self.commentor}"