from django.contrib import admin
from .models import Person, Expense

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'payment_limit')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('person', 'amount', 'category', 'date', 'get_balance')
    
    def get_balance(self, obj):
        return obj.get_balance()
    get_balance.short_description = 'Balance'
