from django import forms


class SearchForm(forms.Form):
    """Used for user input to search."""

    product = forms.CharField(max_length=100, required=False,)
