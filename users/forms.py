"""Define forms and specify custom User model."""
from django.contrib.auth import forms, get_user_model


class UserCreationForm(forms.UserCreationForm):
    """Custom creation form."""

    class Meta(forms.UserCreationForm.Meta):
        """Override the default user with custom user."""

        model = get_user_model()
        fields = ("email",)


class UserChangeForm(forms.UserChangeForm):
    """Custom change form."""

    class Meta(forms.UserChangeForm.Meta):
        """Override the default user with custom user."""

        model = get_user_model()
        fields = forms.UserChangeForm.Meta.fields
