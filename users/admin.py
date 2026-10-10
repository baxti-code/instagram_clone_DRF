from django.contrib import admin
from .models import User, UserConfirmation
# Register your models here.


class UserAdminModel(admin.ModelAdmin):
    list_display = ['id', 'email', 'phone_number']

admin.site.register(User, UserAdminModel)

admin.site.register(UserConfirmation)

