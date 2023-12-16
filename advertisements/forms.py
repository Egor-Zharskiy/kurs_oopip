from django import forms

from advertisements.models import Car


class FilterForm(forms.Form):
    min_price = forms.DecimalField(widget=forms.NumberInput())
    # min_price = forms.DecimalField()
    max_price = forms.DecimalField(widget=forms.NumberInput())

    class Meta:
        fields = ('min_price', 'max_price')
