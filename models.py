from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    payment_limit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Expense(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    date = models.DateField()

    def get_balance(self):
        total_expenses = Expense.objects.filter(person=self.person).aggregate(total=models.Sum('amount'))['total'] or 0
        return self.person.payment_limit - total_expenses

    def __str__(self):
        return f"{self.person.name} - {self.amount}"
