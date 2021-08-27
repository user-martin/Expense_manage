from django import forms
#from django.forms import ModelForm
#from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Layout, Field, ButtonHolder, Submit
from .models import Expense, Income
from django.forms import formset_factory



class DateInput(forms.DateInput):
    input_type = 'date'


class ExpenseForm(forms.ModelForm):

    class Meta:
        model = Expense
        fields = [
            'date',
            'description',
            'type',
            'payment',
            'amount'
        ]
        widgets = {
            'date': DateInput(),
        }

ExpenseFormSet = formset_factory(ExpenseForm, extra=1)



class IncomeForm(forms.ModelForm):

    class Meta:
        model = Income
        fields = [
            'date',
            'description',
            'amount'
        ]
        widgets = {
            'date': DateInput(),
        }
