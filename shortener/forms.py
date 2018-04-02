from django import forms

from shortener.models import Shorten


class ShortenForm(forms.ModelForm):
    class Meta:
        model = Shorten
        fields = ['url']

