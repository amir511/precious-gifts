from django import forms


class ChangeQtyForm(forms.Form):
    new_quantity = forms.IntegerField(min_value=1, help_text="Change requested quantity.")
    item_pk = forms.IntegerField(widget=forms.HiddenInput(), required=False)

