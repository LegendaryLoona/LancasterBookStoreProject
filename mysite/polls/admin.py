from django.contrib import admin

from .models import Investment, Expense

admin.site.register(Investment)
admin.site.register(Expense)
