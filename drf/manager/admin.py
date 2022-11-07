from django.contrib import admin

from .models import Balance, Category, Profile, Transaction

# Register your models here.
admin.site.register(Profile)
admin.site.register(Balance)
admin.site.register(Category)
admin.site.register(Transaction)
