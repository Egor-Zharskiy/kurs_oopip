from django import forms

from advertisements.models import Car


class FilterForm(forms.Form):
    min_price = forms.DecimalField(widget=forms.NumberInput())
    max_price = forms.DecimalField(widget=forms.NumberInput())

    class Meta:
        fields = ('min_price', 'max_price')
