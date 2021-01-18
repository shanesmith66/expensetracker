from django.contrib import admin
from .models import Expense, Budget, Category
# Register your models here.

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("budget", "name", "category", "cost", "date_of_expense")


class ExpenseInline(admin.TabularInline):
    model = Expense
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("budget", "name")

class BudgetAdmin(admin.ModelAdmin):
    list_display = ("name", "budget_amount", "created_at")
    inlines = [
        ExpenseInline
    ]


admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Budget, BudgetAdmin)
admin.site.register(Category, CategoryAdmin)
