from django.forms import ModelForm
from .models import *


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = "__all__"


class bidsForm(ModelForm):
    class Meta:
        model = bids
        fields = "__all__"


class CommentsForm(ModelForm):
    class Meta:
        model = comments
        fields = "__all__"