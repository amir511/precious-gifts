from django import forms

class ChangeQtyForm(forms.Form):
    new_quantity = forms.IntegerField(min_value=1)
    item_pk = forms.IntegerField(widget = forms.HiddenInput(), required = False)