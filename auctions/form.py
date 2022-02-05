from django.forms import ModelForm
from .models import Auction, Bid

class NewAuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'description', 'startBid', 'imageURL', 'category']

class NewBidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['auction', 'bid', 'bidder']
    