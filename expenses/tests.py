from django.test import TestCase
from django.urls import reverse
from .models import Budget
from django.contrib.auth import get_user_model

# Create your tests here.
class BudgetTests(TestCase):

    def setUp(self):
        User = get_user_model()
        user =  User.objects.create_user(
            username='will',
            email='will@email.com',
            password='testpass123'
        )
        self.budget = Budget.objects.create (
            name = 'Test',
            budget_amount = 69420,
            user_id = user.id,
        )

    def test_budget_listing(self):
        self.assertEqual(f'{self.budget.name}', 'Test')
        self.assertEqual(self.budget.budget_amount, 69420)

    def test_budget_list_view(self):
        response = self.client.get(reverse('expense_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')
        self.assertTemplateUsed(response, 'expenses/budget_list.html')

    def test_budget_detail_view(self):
        response = self.client.get(self.budget.get_absolute_url())
        no_response = self.client.get('/expenses/2312321312')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Test')
        self.assertTemplateUsed(response, 'expenses/budget_detail.html')