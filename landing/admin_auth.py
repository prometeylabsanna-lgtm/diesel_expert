from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import User
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from landing.admin_filters import UkRelatedDropdownFilter, YesNoDropdownFilter
from landing.admin_mixins import TopFiltersMixin

if admin.site.is_registered(User):
    admin.site.unregister(User)


@admin.register(User)
class UserAdmin(TopFiltersMixin, DjangoUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    search_help_text = "Ім’я або email"
    list_filter = (
        ("is_staff", YesNoDropdownFilter),
        ("is_superuser", YesNoDropdownFilter),
        ("is_active", YesNoDropdownFilter),
        ("groups", UkRelatedDropdownFilter),
    )
    list_filter_options = {
        "is_staff": {"label": "Персонал", "horizontal": True},
        "is_superuser": {"label": "Суперкористувач", "horizontal": True},
        "is_active": {"label": "Активний", "horizontal": True},
        "groups": {"label": "Групи", "horizontal": True},
    }
