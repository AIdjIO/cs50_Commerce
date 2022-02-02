from asyncio.windows_events import NULL
from xml.dom.pulldom import parseString
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Auction(models.Model):
    creationDate = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length = 64, default='')
    description = models.TextField(default='')
    startBid = models.DecimalField(max_digits=19, decimal_places=2)
    imageURL = models.URLField(default='')
    category = models.CharField(max_length = 40, default='')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")

    def __str__(self):
        return f"{self.title} ${self.startBid} {self.category} started at {self.creationDate} sold by {self.seller}"

class WatchList(models.Model):
    watching = models.ForeignKey(Auction, on_delete=models.PROTECT, related_name="auction", default=NULL)
    watcher = models.ForeignKey(User, on_delete=models.PROTECT, related_name="watcher")

class Bid(models.Model):
    bidDate = models.DateTimeField(auto_now_add=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids", default=0)
    bid = models.DecimalField(max_digits=12, decimal_places=2, default=0.01)
    bidder = models.ManyToManyField(User, related_name="bidder")
    
    def __str__(self):
        return f"{self.auction} {self.bid} @{self.bidDate} by {self.bidder}"

class Comment(models.Model):
    creationDate = models.DateTimeField(auto_now_add=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comment", default=0)
    comment= models.TextField(default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")

    def __str__(self):
        return f"{self.comment} on {self.creationDate}, extract:{(self.comment)[0-50]}"