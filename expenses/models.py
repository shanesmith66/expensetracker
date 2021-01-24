from django.db import models
from django.contrib.auth import get_user_model
from .utils import generate_unique_slug
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
class Budget(models.Model):
    created_at = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    budget_amount = models.IntegerField()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=get_user_model())
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['slug'], name='slug_index')
        ]

    def save(self, *args, **kwargs):
        if self.slug:  # edit
            if slugify(self.name) != self.slug:
                self.slug = generate_unique_slug(Budget, self.name)
        else:  # create
            self.slug = generate_unique_slug(Budget, self.name)
        super(Budget, self).save(*args, **kwargs)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('budget_detail', args=[str(self.slug)])

    def budget_spent(self):
        expense_list = Expense.objects.filter(budget=self)
        total_expense_amount = 0
        for expense in expense_list:
            total_expense_amount += expense.cost

        return int(total_expense_amount)

    def category_names(self):
        category_list = Category.objects.filter(budget=self)
        names = [category.name for category in category_list]
        return names

        




class Category(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Expense(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='expenses')
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_expense = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('budget_detail', args=[str(self.budget.slug)])


