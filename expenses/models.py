from django.db import models

# Create your models here.
class Expense(models.Model):
    item_name = models.CharField(max_length=200)
    category_name = models.CharField(max_length=200)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_expense = (models.DateField(auto_now_add=True))

    def __str__(self):
        return self.item_name
