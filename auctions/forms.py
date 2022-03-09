
from cProfile import label
from dataclasses import fields
from django import forms
from django.forms import ModelForm
from .models import Bid, Listing, Comment

CATEGORY_CHOICES = (
            ('electronics', 'Electronics'),
            ('household', 'Household'),
            ('kitchen', 'Kitchen'),
            ('outdoors', 'Outdoors'),
            ('toys', 'Toys'),
            ('cleaning', 'Cleaning'),
            ('apparel', 'Apparel'),
        )

class NewListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'category', 'description', 'price','image_url']
        
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control','placeholder':'This is the Title of your item'}),
            'description':forms.Textarea(attrs={'class':'form-control','placeholder':'You can a description here..'}),
            'price':forms.NumberInput(attrs={'class':'form-control'}),
            'category': forms.Select(choices=CATEGORY_CHOICES, attrs={'class': 'form-control'}),
            'image_url':forms.URLInput(attrs={'class':'form-control'})
        }


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        widgets={
            'amount':forms.NumberInput(attrs={'class':'form-control','placeholder':'Add an appropriate asking price...'})
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_desc']
        widgets={
            'comment_desc':forms.Textarea(attrs={'class':'form-control','placeholder':'You can add a comment here...'})
        }
        labels={
            'comment_desc':'Add Comment'
        }
