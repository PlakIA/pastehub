from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

import users.models


admin.site.register(users.models.CustomUser, UserAdmin)
