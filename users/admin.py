from django.contrib import admin
from users.models import *
from unfold.admin import ModelAdmin as UnfoldAdmin


@admin.register(CustomUser)
class CustomUserAdmin(UnfoldAdmin):
    list_display = ('id', 'full_name', 'phone', 'password', 'status')


@admin.register(CodeVerification)
class CodeVerificationAdmin(UnfoldAdmin):
    list_display = ('id', 'user', 'code')