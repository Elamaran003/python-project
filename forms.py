from django import forms
from .models import Expense,Person

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['person', 'amount', 'category', 'date']
        


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'email', 'payment_limit']


