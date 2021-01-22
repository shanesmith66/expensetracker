from django.urls import path
from .views import BudgetListView, BudgetDetailView, BudgetCreateView, BudgetDeleteView, BudgetUpdateView

urlpatterns = [
    path('<slug:slug>/edit/', BudgetUpdateView.as_view(), name='budget_edit'),
    path('<slug:slug>', BudgetDetailView.as_view(), name='budget_detail'),
    path('<slug:slug>/delete/', BudgetDeleteView.as_view(), name='budget_delete'),
    path('create/', BudgetCreateView.as_view(), name='budget_create'),
    path('', BudgetListView.as_view(), name='expense_list'),

]