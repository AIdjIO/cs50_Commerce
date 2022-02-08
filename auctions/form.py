from django.forms import ModelForm
from .models import Auction, Bid

class NewAuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'description', 'startBid', 'imageURL', 'category']

    def __init__(self, *args, **kwargs):
        super(NewAuctionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class NewBidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid', 'bidder', 'auction']
        ordering = ('-bid',)
    
    def __init__(self, *args, **kwargs):
        super(NewBidForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'