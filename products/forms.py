from django import forms

PRODUCT_AMOUNT_CHOICES = [(i, str(i)) for i in range(1,11)]

class CartAddProductForm(forms.Form):
    amount = forms.TypedChoiceField(choices=PRODUCT_AMOUNT_CHOICES, coerce=int)
    override_amount = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
