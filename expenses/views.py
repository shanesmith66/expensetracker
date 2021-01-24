from django.shortcuts import render, get_object_or_404, reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, FormMixin, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Budget, Expense, Category
from .forms import ExpenseForm
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.utils.text import slugify
from django.contrib.auth import get_user_model
import json
from django.db.models import Sum


class BudgetDeleteView(LoginRequiredMixin, DeleteView):
    model = Budget
    template_name = 'expenses/budget_delete.html'
    success_url = reverse_lazy('expense_list')
    login_url = 'account_login'

class BudgetUpdateView(LoginRequiredMixin, UpdateView):
    model = Budget
    template_name = 'expenses/budget_edit.html'
    fields = ('name', 'budget_amount')
    login_url = 'account_login'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        categories = self.request.POST['categoriesString'].split(",")

        for category in categories:
            if category != '' and category not in self.object.category_names():
                Category.objects.create (
                    budget=Budget.objects.get(id=self.object.id),
                    name=category
                ).save()

        return HttpResponseRedirect(self.get_success_url())



class BudgetDetailView(LoginRequiredMixin, UserPassesTestMixin, FormMixin, DetailView):
    model = Budget
    template_name = 'expenses/budget_detail.html'
    slug_field = 'slug'
    form_class = ExpenseForm
    login_url = 'account_login'

    def test_func(self):
        current_user = self.get_object()
        return self.request.user == current_user.user

    def get_initial(self):
        return {"budget": self.get_object() }

    def get_success_url(self):
        return reverse('budget_detail', kwargs={"slug": self.object.slug})

    def get_context_data(self, **kwargs):
        context = super(BudgetDetailView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()

        # filter the queryset
        context['form'].fields['category'].queryset = Category.objects.filter(budget=self.object) 
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            name = form.cleaned_data['name']
            cost = form.cleaned_data['cost']
            category_name = form.cleaned_data['category']

            category = get_object_or_404(Category, budget=self.object, name=category_name)

            Expense.objects.create(
                budget=self.object,
                category=category,
                name=name,
                cost=cost
            ).save()

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def delete(self, request, *args, **kwargs):
        id = json.loads(request.body)['id']
        expense = get_object_or_404(Expense, id=id)
        expense.delete()

        return HttpResponse('')

    def form_valid(self, form):
        return super(BudgetDetailView, self).form_valid(form)


# group expenses by category to make a bar chart
def spending_chart(request):
    labels = [] 
    data = []

    # extract slug from url
    path = request.META.get('HTTP_REFERER')
    path = path.rsplit('/', 1)
    budget_slug = path[-1]

    # get budget
    budget = get_object_or_404(Budget, slug=budget_slug)

    category_list = Category.objects.filter(budget=budget)

    for category in category_list:

        queryset = Expense.objects.filter(category__name=category).filter(budget=budget).values('category__name').annotate(category_cost=Sum('cost')).order_by('-category_cost')
        for entry in queryset:
            labels.append(entry['category__name'])
            data.append(entry['category_cost'])
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })


class BudgetListView(LoginRequiredMixin, ListView):
    model = Budget
    template_name = 'expenses/budget_list.html'
    login_url = 'account_login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        context['object_list'] = Budget.objects.filter(user = current_user)
        return context


class BudgetCreateView(LoginRequiredMixin, CreateView):
    model = Budget
    template_name = 'expenses/budget_create.html'
    fields = ('name', 'budget_amount')
    login_url = 'account_login'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        categories = self.request.POST['categoriesString'].split(",")

        for category in categories:
            print(self.object.categories)
            Category.objects.create (
                budget=Budget.objects.get(id=self.object.id),
                name=category
            ).save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('budget_detail', kwargs={"slug": self.object.slug})
