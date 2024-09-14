from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('add/', views.add_expense, name='add_expense'),
    path('edit/<int:pk>/', views.edit_expense, name='edit_expense'),
    path('delete/<int:pk>/', views.delete_expense, name='delete_expense'),
    path('add name/', views.add_person, name='add_person'),
    path('export_csv/', views.export_csv, name='export_csv'),
   
]
