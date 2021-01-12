from django.contrib import admin
from .models import Expense
# Register your models here.

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("item_name", "category_name", "cost", "date_of_expense")

admin.site.register(Expense, ExpenseAdmin)
