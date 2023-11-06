from django import forms


class FilterForm(forms.Form):
    min_price = forms.DecimalField(widget=forms.NumberInput())
    # min_price = forms.DecimalField()
    max_price = forms.DecimalField(widget=forms.NumberInput())

    class Meta:
        fields = ('min_price', 'max_price')
