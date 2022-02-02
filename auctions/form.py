from django.forms import ModelForm
from .models import Auction

class NewAuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'description', 'startBid', 'imageURL', 'category']
    