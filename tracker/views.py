from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django_tables2 import RequestConfig
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.forms.models import modelformset_factory
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum, Count, CharField, Value
from django.template.loader import render_to_string
from django.db import models
from django.core.paginator import Paginator
from .models import Expense, Income
from .forms import ExpenseForm, IncomeForm, ExpenseFormSet
from .utils import AmountUnitUtil
import random
from calendar import monthrange
from datetime import datetime as dt
import json
from itertools import chain
import pandas as pd






def expense_list(request):
    expenses_list = Expense.objects.filter(created_by=request.user)
    paginator = Paginator(expenses_list, 10)
    page_number = request.GET.get('page')
    expenses = paginator.get_page(page_number)
    return render(request, 'tracker/index_expense.html', {'expenses': expenses})

def save_expense_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            expenses = Expense.objects.filter(created_by=request.user)
            data['html_expense_list'] = render_to_string('tracker/expense_include/expense_list.html', {
                'expenses': expenses
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def save_new_expense_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.created_at = dt.now()
            form = obj.save()
            data['form_is_valid'] = True
            expenses = Expense.objects.filter(created_by=request.user)
            data['html_expense_list'] = render_to_string('tracker/expense_include/expense_list.html', {
                'expenses': expenses
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
    else:
        form = ExpenseForm()
    return save_new_expense_form(request, form, 'tracker/expense_include/expense_create.html')

def expense_set(request):
    data=dict()
    template_name = 'tracker/expense_include/expense_formset_create.html'
    if request.method == 'GET':
        formset = ExpenseFormSet(request.GET or None)
    elif request.method == 'POST':
        formset = ExpenseFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                obj = form.save(commit=False)
                obj.created_by = request.user
                obj.created_at = dt.now()
                form = obj.save()
                # extract name from each form and save

                data['form_is_valid'] = True
                expenses = Expense.objects.filter(created_by=request.user)
                data['html_expense_list'] = render_to_string('tracker/expense_include/expense_list.html', {
                    'expenses': expenses
                })
        else:
            data['form_is_valid'] = False
    context = {'formset': formset}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def expense_Update_set(request):
    data=dict()
    template_name = 'tracker/expense_include/expense_formset_update.html'
    expense_formset = modelformset_factory(Expense, form=ExpenseForm, extra =0 )
    queryset = Expense.objects.filter(created_by=request.user)

    if request.method == 'GET':
        formset = expense_formset(request.POST or None, queryset=queryset)

    elif request.method == 'POST':
        formset = expense_formset(request.POST or None, queryset=queryset)
        if formset.is_valid():
            for form in formset:
                obj = form.save(commit=False)
                form = obj.save()

                data['form_is_valid'] = True
                expenses = Expense.objects.filter(created_by=request.user)
                data['html_expense_list'] = render_to_string('tracker/expense_include/expense_list.html', {
                    'expenses': expenses
                })
        else:
            data['form_is_valid'] = False

    context = {'formset': formset}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
    else:
        form = ExpenseForm(instance=expense)
    return save_expense_form(request, form, 'tracker/expense_include/expense_update.html')


def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    data = dict()
    if request.method == 'POST':
        expense.delete()
        data['form_is_valid'] = True
        expenses = Expense.objects.filter(created_by=request.user)
        data['html_expense_list'] = render_to_string('tracker/expense_include/expense_list.html', {
            'expenses': expenses
        })
    else:
        context = {'expense': expense}
        data['html_form'] = render_to_string('tracker/expense_include/expense_delete.html', context, request=request)
    return JsonResponse(data)



def income_list(request):
    incomes = Income.objects.filter(created_by=request.user)
    return render(request, 'tracker/index_income.html', {'incomes': incomes})

def save_income_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            incomes = Income.objects.filter(created_by=request.user)
            data['html_income_list'] = render_to_string('tracker/income_include/income_list.html', {
                'incomes': incomes
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)

def save_new_income_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.created_at = dt.now()
            form = obj.save()
            data['form_is_valid'] = True
            incomes = Income.objects.filter(created_by=request.user)
            data['html_income_list'] = render_to_string('tracker/income_include/income_list.html', {
                'incomes': incomes
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def income_create(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
    else:
        form = IncomeForm()
    return save_new_income_form(request, form, 'tracker/income_include/income_create.html')


def income_update(request, pk):
    income = get_object_or_404(Income, pk=pk)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
    else:
        form = IncomeForm(instance=income)
    return save_income_form(request, form, 'tracker/income_include/income_update.html')


def income_delete(request, pk):
    income = get_object_or_404(Income, pk=pk)
    data = dict()
    if request.method == 'POST':
        income.delete()
        data['form_is_valid'] = True
        incomes = Income.objects.filter(created_by=request.user)
        data['html_income_list'] = render_to_string('tracker/income_include/income_list.html', {
            'incomes': incomes
        })
    else:
        context = {'income': income}
        data['html_form'] = render_to_string('tracker/income_include/income_delete.html', context, request=request)
    return JsonResponse(data)




class AnalyticsView(generic.ListView):
    template_name = "analytics/index.html"
    context_object_name = "records"
    model = Expense

    def statistic(request):
        # init
        avg_year = 0
        avg_month = 0
        avg_day = 0

        # get user expense objects
        exp = Expense.objects.filter(created_by=request.user)

        # count total record
        total_records = exp.count()

        # sum up all the expenses
        total_expenses = exp.aggregate(amount=Sum('amount'))['amount']
        if total_expenses is None:
            total_expenses = 0

        # categories count
        categories = exp.values('type').annotate(the_count=Count('type')).count()

        # list out dates for the following processing.
        dates = list(exp.values('date')
                     .values_list('date', flat=True))

        # avg amount per year, per month and per day
        year_arr = []
        month_arr = []
        day_arr = []

        for date in dates:
            if date.year not in year_arr:
                year_arr.append(date.year)
            if date.year not in month_arr:
                month_arr.append(date.month)
            if date.year not in day_arr:
                day_arr.append(date.day)

        if total_expenses > 0 :
            avg_year = AmountUnitUtil.convertToMills(total_expenses / year_arr.__len__())
            avg_month = AmountUnitUtil.convertToMills(total_expenses / month_arr.__len__())
            avg_day = AmountUnitUtil.convertToMills(total_expenses / day_arr.__len__())
            total_expenses = AmountUnitUtil.convertToMills(total_expenses)

        now = dt.now()

        context = {
            'context_type': 'statistic',
            'total_records': total_records,
            'total_expenses': total_expenses,
            'categories': categories,
            'avg_year': avg_year,
            'avg_month': avg_month,
            'avg_day': avg_day,
            'current_year': now.year,
            'current_month': now.month,
            'current_day': now.day

        }

        return render(request, "analytics/index.html", context)

    def annually(request, year):
        # get user expense objects
        exp = Expense.objects.filter(created_by=request.user)

        # retrieve distinct types
        expense_type = list(exp.filter(date__year=year).values('type').distinct().order_by()
                                 .values_list('type', flat=True))

        datasets = []
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November", "December"]

        for type in expense_type:
            # expense
            arr = list(exp.filter(date__year=year).filter(type=type).distinct().order_by('date'))

            # expense month by type
            month_tmp_arr = list(exp.filter(date__year=year).filter(type=type).values('date').distinct()
                            .order_by('date')
                            .values_list('date', flat=True))

            # expense amount by type
            expense_tmp_arr = list(exp.filter(date__year=year).filter(type=type)
                .values('date').distinct().order_by('date')
                .annotate(amount=Sum('amount')).values_list('amount', flat=True))

            # init array with size 12 with value 0
            monthly_expense_cnt = [0] * 12

            for i, m in enumerate(arr):
                monthly_expense_cnt[m.date.month-1] += m.amount

            total_amount = []

            for j, k in enumerate(monthly_expense_cnt):
                o = {}
                o['x'] = months[j];
                o['y'] = monthly_expense_cnt[j];
                total_amount.append(o)

            # generate random color
            r = lambda: random.randint(0, 255)
            color = '#%02X%02X%02X' % (r(), r(), r())

            # construct dataset
            dataset = {
                'label': type,
                'backgroundColor': color,
                'borderColor': color,
                'data': total_amount,
                'fill': 'false'
            }

            datasets.append(dataset)

        # fetch available years for menu labels
        dates = list(exp.values('date')
             .values_list('date', flat=True))
        year_arr = []
        for date in dates:
            if date.year not in year_arr:
                year_arr.append(date.year)
        year_arr.sort()

        # construct submenu
        expense_per_month = []
        month_not_none = []
        for i, month in enumerate(months):
            amount = exp.filter(date__year=year).filter(date__month=(i+1)).values('date').distinct().order_by('date').aggregate(amount=Sum('amount'))['amount']
            if amount is not None:
                expense_per_month.append(float("{0:.2f}".format(amount)))
                month_not_none.append((months[i]))


        if expense_per_month:
            submenu = zip(month_not_none, expense_per_month)
        else:
            submenu = False

        context = {
            'context_type': 'annually',
            'datasets': datasets,
            'labels': months,
            'title': 'Annual Report in ' + str(year),
            'report_type': 'line',
            'menu_labels': year_arr,
            'x_axis_label': 'Month',
            'submenu': submenu
        }

        return render(request, "analytics/index.html", context)

    def monthly(request, year, month):
        # get user expense objects
        exp = Expense.objects.filter(created_by=request.user)

        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November", "December"]
        months_reverse = dict(January=1, February=2, March=3, April=4)
        datasets = []

        # retrieve distinct types
        expense_type = list(exp.filter(date__year=year).filter(date__month=month).values('type').distinct().order_by()
                            .values_list('type', flat=True))

        lastday = monthrange(year, month)[1]
        days = list(range(1,lastday+1))

        for type in expense_type:
            # expense
            arr = list(exp.filter(date__year=year).filter(date__month=month).filter(type=type).distinct().order_by('date'))

            # expense month by type
            month_tmp_arr = list(exp.filter(date__year=year).filter(date__month=month).filter(type=type).values('date').distinct()
                                 .order_by('date')
                                 .values_list('date', flat=True))

            # expense amount by type
            expense_tmp_arr = list(exp.filter(date__year=year).filter(date__month=month).filter(type=type)
                                   .values('date').distinct().order_by('date')
                                   .annotate(amount=Sum('amount')).values_list('amount', flat=True))

            # init array
            daily_expense_cnt = [0] * lastday

            for i, m in enumerate(arr):
                daily_expense_cnt[m.date.day] += m.amount

            total_amount = []

            for j, k in enumerate(daily_expense_cnt[1:]):
                o = {}
                o['x'] = days[j];
                o['y'] = daily_expense_cnt[j+1];
                total_amount.append(o)

            # generate random color
            r = lambda: random.randint(0, 255)
            color = '#%02X%02X%02X' % (r(), r(), r())

            # construct dataset
            dataset = {
                'label': type,
                'backgroundColor': color,
                'borderColor': color,
                'data': total_amount,
                'fill': 'false'
            }

            datasets.append(dataset)

        # fetch available months for menu labels
        dates = list(exp.values('date')
                     .values_list('date', flat=True))
        month_arr = []
        month_labels = []
        for date in dates:
            if date.month not in month_arr:
                month_arr.append(date.month)
                month_arr.sort()

        for single_month in month_arr:
            month_labels.append(months[single_month - 1])
        # construct submenu
        expense_per_day = []
        day_not_none  = []
        for i, d in enumerate(days):
            amount = exp.filter(date__year=year).filter(date__month=month).filter(date__day=(i+1)).values('date').distinct().order_by(
                'date').aggregate(amount=Sum('amount'))['amount']
            if amount is not None:
                expense_per_day.append(float("{0:.2f}".format(amount)))
                day_not_none.append((i+1))

        if expense_per_day:
            submenu = zip(day_not_none, expense_per_day)
        else:
            submenu = False

        context = {
            'context_type': 'monthly',
            'datasets': datasets,
            'monthly_expense': expense_type,
            'labels': days,
            'title': 'Monthly Report on ' + str(months[month-1]) + ' ' + str(year),
            'report_type': 'bar',
            'selected_year':year ,
            'menu_labels': month_arr,
            'month_labels': month_labels,
            'x_axis_label': 'Day',
            'submenu': submenu,
            'months': months
        }
        return render(request, "analytics/index.html", context)

    def daily(request, year, month, day):
        # get user expense objects
        exp = Expense.objects.filter(created_by=request.user)

        type =[]
        # retrieve distinct types
        expense_type = list(
            exp.filter(date__year=year).filter(date__month=month)
            .filter(date__day=day).values('type').distinct().order_by()
            .values_list('type', flat=True))

        datasets = []
        expense_arr = []
        color_arr = []
        for type in expense_type:
            # expense amount by type
            expense_tmp_arr = list(exp.filter(date__year=year).filter(date__month=month).filter(date__day=day)
                                   .filter(type=type)
                                   .values('date').distinct().order_by('date')
                                   .annotate(amount=Sum('amount')).values_list('amount', flat=True))
            # get the sum
            expense_arr.append(expense_tmp_arr[0])

            # generate random color
            r = lambda: random.randint(0, 255)
            color = '#%02X%02X%02X' % (r(), r(), r())
            color_arr.append(color)

        # construct dataset
        if color_arr and expense_arr:
            dataset = {
                'label': type,
                'backgroundColor': color_arr,
                'borderColor': color_arr,
                'data': expense_arr
            }
            datasets.append(dataset)

        # construct submenu
        expense_per_type = []
        for i, type in enumerate(expense_type):
            amount = exp.filter(date__year=year).filter(date__month=month).filter(date__day=day).filter(type=type).values('date').distinct().order_by('date').aggregate(amount=Sum('amount'))['amount']
            if amount is not None:
                expense_per_type.append(float("{0:.2f}".format(amount)))

        if expense_per_type:
            submenu = zip(expense_type, expense_per_type)
        else:
            submenu = False

        context = {
            'context_type': 'daily',
            'datasets': datasets,
            'daily_expense': expense_type,
            'labels': expense_type,
            'title': 'Daily Report on ' + str(day) + '/' + str(month) + '/' + str(year) ,
            'x_axis_label': 'Type',
            'report_type': 'pie',
            'submenu': submenu
        }
        return render(request, "analytics/index.html", context)


class MainView():

    def main(request):

        month_list = {"January":1, "February":2, "March":3, "April":4, "May":5, "June":6, "July":7, "August":8, "September":9, "October":10,
                  "November":11, "December":12}

        res = []

        filter_category = request.GET.get("filter_category")


        this_year = dt.now().year
        present_month = dt.now().month

        this_month = filter_category or present_month



        total_expense = Expense.objects.filter(created_by=request.user,date__year=this_year,date__month=this_month).aggregate(Sum("amount"))
        total_income = Income.objects.filter(created_by=request.user,date__year=this_year,date__month=this_month).aggregate(Sum("amount"))
        type = list(Expense.objects.filter(created_by=request.user,date__year=this_year,date__month=this_month).values_list("description","amount"))
        res = [list(ele) for ele in type]
        head = ['description','amount']
        res.insert(0,head)

        total_spent = (total_expense["amount__sum"])
        total_salary = (total_income["amount__sum"])



        balance = total_salary - total_spent

# table_main
        total_expense1 = Expense.objects.filter(created_by=request.user,date__month=this_month,date__year=this_year).values("date","description","amount").annotate(Type=Value('Debited', output_field=CharField()))
        total_income1 = Income.objects.filter(created_by=request.user,date__month=this_month,date__year=this_year).values("date","description","amount").annotate(Type=Value('Credited', output_field=CharField()))
        result_list = list(chain(total_expense1, total_income1))
        df = pd.DataFrame(result_list)
        df_sort=df.sort_values(by='date').reset_index(drop=True)


        table_content = df_sort.to_html(index=False)



        context = {

        'month_list':month_list,
        'total_spent':total_spent,
        'total_salary':total_salary,
        'balance':balance,
        'array': json.dumps(res),
        'table_content': table_content
        }
        if filter_category:
            return render(request, "tracker/index_main_content.html", context)
        else:
            return render(request, "tracker/index_main.html", context)


def export_pdf(request):

    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = 'attachment; filename = Expense' + \
        str(dt.now())+'.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    html_string = render_to_string('tracker/expense_include/export_pdf.html',{'expenses': []})
    html = HTML(string=html_string)

    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:

        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    return response
