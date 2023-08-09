from django.contrib import admin
from .models import Customer,Account
# Register your models here.

class customerAdmin(admin.ModelAdmin):
    list_display = ['username','phone_number','email']


admin.site.register(Customer,customerAdmin)

class CustomerAccount(admin.ModelAdmin):
    list_display =['account_number','customer','balance']

admin.site.register(Account,CustomerAccount)