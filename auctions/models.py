from xml.dom.pulldom import parseString
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    auctionTitle = models.CharField(max_length = 64)
    auctionDescription = models.TextField()
    auctionStartBid = models.DecimalField(max_digits=19, decimal_places=2)
    auctionImageURL = models.URLField()
    auctionCategory = models.CharField(max_length = 40)

    def __str__(self):
        return f"{self.auctionTitle} {self.auctionDescription} ${self.auctionStartBid} {self.auctionCategory}"

class Bids(models.Model):
    bidsOnListing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="listingBids")
    bid = models.DecimalField(max_digits=19, decimal_places=2, default=0.99)
    
    def __str__(self):
        return f"{self.auctionListing} {self.bid}"

class Comment(models.Model):
    commentOnListing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="listingComments")
    comments= models.TextField()
    pass