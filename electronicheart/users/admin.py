from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from electronicheart.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    # This field "fieldsets" is a tuple of tuples, which in turn consist of a string and a dict. These individual tuple
    # elements each define one section in the admin detail edit page. The first element (the string) is the title of
    # the section and the second element (the dict) defines how this section is structured.
    fieldsets = (
        (
            "User",
            {"fields": ("name", "image", "bio")}
        ),
    ) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]
