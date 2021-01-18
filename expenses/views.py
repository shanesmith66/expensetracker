from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, FormMixin
from .models import Budget, Expense, Category
from .forms import ExpenseForm
from django.http import HttpResponseRedirect



class BudgetDetailView(FormMixin, DetailView):
    model = Budget
    template_name = 'expenses/budget_detail.html'
    slug_field = 'slug'
    form_class = ExpenseForm


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
            print('xD')
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

    def form_valid(self, form):
        return super(BudgetDetailView, self).form_valid(form)

class BudgetListView(ListView):
    model = Budget
    template_name = 'expenses/budget_list.html'

class BudgetCreateView(CreateView):
    model = Budget
    template_name = 'expenses/budget_create.html'
    fields = ('name', 'budget_amount', 'user')

