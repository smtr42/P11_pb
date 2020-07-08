"""Admin specifications to use the User custom model."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.forms import UserChangeForm, UserCreationForm

from .models import User


class UserAdmin(BaseUserAdmin):
    """Update admin.py to use custom user model."""

    model = User
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = [
        "email",
        "username",
    ]


admin.site.register(User, UserAdmin)
