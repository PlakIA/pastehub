from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

import users.models


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = users.models.CustomUser


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("image",)}),)


admin.site.register(users.models.CustomUser, MyUserAdmin)
