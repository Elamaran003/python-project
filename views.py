from django.http import HttpResponse
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from .models import Expense,Person
from .forms import ExpenseForm, PersonForm#
from tracker import models
import csv#


#def home(request):
    #expenses = Expense.objects.all()
    #total_balance = sum(expense.get_balance() for expense in expenses)
    #context = {
        #'expenses': expenses,
        #'total_balance': total_balance,
    #}
    #return render(request, 'tracker/home.html', context)

def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ExpenseForm()
    return render(request, 'tracker/add_expense.html', {'form': form})


def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'tracker/edit_expense.html', {'form': form})


def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        expense.delete()
        return redirect('home')
    return render(request, 'tracker/delete_expense.html', {'expense': expense})


def update_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            # Calculate the updated balance for the person
            total_expenses = Expense.objects.filter(person=expense.person).aggregate(total=models.Sum('amount'))['total'] or 0
            updated_balance = expense.person.payment_limit - total_expenses
            # Update the total balance in the person's record
            expense.person.save()
            return redirect('home')
    else:
        form = ExpenseForm(instance=expense)
    
    # balamce calculation before updating
    total_expenses = Expense.objects.filter(person=expense.person).aggregate(total=models.Sum('amount'))[''] or 0
    initial_balance = expense.person.payment_limit - total_expenses

    return render(request, 'tracker/update_expense.html', {
        'form': form,
        'initial_balance': initial_balance,
        'updated_balance': expense.get_balance(),
    })
    
    
    
def add_person(request):##
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to home or another page after saving
    else:
        form = PersonForm()
    
    return render(request, 'tracker/add_person.html', {'form': form})



def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=persons.csv'

    writer = csv.writer(response)
    writer.writerow(['name', 'email', 'payment_limit'])
    

    persons = Person.objects.all().values_list('name', 'email', 'payment_limit')
    for person in persons:
        writer.writerow(person)

    return response


def home(request):
    persons = Person.objects.all()
    expenses = Expense.objects.all()
    messages = []

    # check if they exceed the payment limit
    for person in persons:
        total_expenses = Expense.objects.filter(person=person).aggregate(Sum('amount'))['amount__sum'] or 0
        balance = person.payment_limit - total_expenses

        # Check the balance is zero or negative
        if balance <= 0:
            messages.append(f"{person.name}, you are exceeding your payment limit!")

    context = {
        'persons': persons,
        'expenses': expenses,
        'messages': messages,  # Passing the messages to the template
    }
    return render(request, 'tracker/home.html', context)
    
    
    
    
    
