from asyncio.windows_events import NULL
from xml.dom.pulldom import parseString
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class User(AbstractUser):
	def __str__(self):
		return f"{self.username}"

class Auction(models.Model):
	creationDate = models.DateTimeField(auto_now_add=True)
	title 		 = models.CharField(max_length = 64, default='')
	description  = models.TextField(default='')
	startBid 	 = models.DecimalField(max_digits=12, decimal_places=2,validators=[MinValueValidator(0.0)], default=0.01)
	imageURL 	 = models.URLField(default='')
	category 	 = models.CharField(max_length = 40, default='')
	seller 		 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
	ended 		 = models.BooleanField(default = False)

	class Meta:
		ordering = ('-creationDate',)

	def hasEnded(self):
		return self.ended
	
	def endAuction(self):
		self.ended = True

	def maxBid(self):
		Bid.objects.get(id = self.id)

	def __str__(self):
		return f"{self.title} ${self.startBid} {self.category} started at {self.creationDate} sold by {self.seller}"

class WatchList(models.Model):
	watching = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='auction', default=NULL)
	watcher  = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watcher")

	def __str__(self):
		return f"{self.watching} {self.watcher}"

class Bid(models.Model):
	bidDate = models.DateTimeField(auto_now_add=True)
	auction = models.ForeignKey(Auction, on_delete=models.CASCADE, default=0,related_name='bids')
	bid     = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], default=0.01)
	bidder  = models.ForeignKey(User,on_delete=models.PROTECT, related_name="currentBidder")

	class Meta:
		ordering = ('-bid',)
	
	def __str__(self):
		return f"{self.auction} {self.bid} @{self.bidDate} by {self.bidder}"

class Comment(models.Model):
	creationDate = models.DateTimeField(auto_now_add=True)
	auction 	 = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comment", default=0)
	comment 	 = models.TextField(default='')
	user 		 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")

	class Meta:
		ordering = ('-creationDate',)
	
	def __str__(self):
		return f"{self.comment} on {self.creationDate}, extract:{(self.comment)}"