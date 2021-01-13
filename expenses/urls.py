from django.urls import path
from .views import BudgetListView, BudgetDetailView

urlpatterns = [
    path('<slug:slug>', BudgetDetailView.as_view(), name='budget_detail'),
    path('', BudgetListView.as_view(), name='expense_list'),
]