from django.urls import path
from .views import BudgetListView, BudgetDetailView, BudgetCreateView

urlpatterns = [
    path('<slug:slug>', BudgetDetailView.as_view(), name='budget_detail'),
    path('create/', BudgetCreateView.as_view(), name='budget_create'),
    path('', BudgetListView.as_view(), name='expense_list'),

]