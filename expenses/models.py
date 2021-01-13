from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

# Create your models here.
class Budget(models.Model):
    created_at = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    budget_amount = models.IntegerField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Budget, self).save(*args, **kwargs)


class Category(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class Expense(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='expenses')
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_expense = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
