from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Expense, Budget, Category


class BudgetDetailView(DetailView):
    model = Budget
    template_name = 'expenses/budget_detail.html'
    slug_field = 'slug'
# Create your views here.
class BudgetListView(ListView):
    model = Budget
    template_name = 'expenses/budget_list.html'

