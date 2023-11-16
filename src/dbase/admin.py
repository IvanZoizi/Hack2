from django.contrib import admin
from .models import User


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, AuthorAdmin)