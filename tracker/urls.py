from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'tracker'

urlpatterns = [
	# /
    path('', views.landingView.landing, name ="landing"),


    # /tracker
    path('tracker', login_required(views.MainView.main), name ="main"),


    # /analytics
    path('analytics', login_required(views.AnalyticsView.statistic), name="analytics"),

    # /analytics/2018
    path('analytics/<int:year>', login_required(views.AnalyticsView.annually), name="annually"),

    # /analytics/2018/02
    path('analytics/<int:year>/<int:month>', login_required(views.AnalyticsView.monthly), name="monthly"),

    # /analytics/2018/02/20
    path('analytics/<int:year>/<int:month>/<int:day>', login_required(views.AnalyticsView.daily), name="daily"),


    re_path(r'^tracker/$', views.expense_list, name='expense_list'),
    re_path(r'^tracker/create/$', views.expense_create, name='expense_create'),
    re_path(r'^tracker/create_set/$', views.expense_set, name='expense_create_formset'),
    re_path(r'^tracker/update_set/$', views.expense_Update_set, name='expense_update_formset'),
    re_path(r'^tracker/(?P<pk>\d+)/update/$', views.expense_update, name='expense_update'),
    re_path(r'^tracker/(?P<pk>\d+)/delete/$', views.expense_delete, name='expense_delete'),


    re_path(r'^tracker/income/$', views.income_list, name='income_list'),
    re_path(r'^tracker/income/create/$', views.income_create, name='income_create'),
    re_path(r'^tracker/income/(?P<pk>\d+)/update/$', views.income_update, name='income_update'),
    re_path(r'^tracker/income/(?P<pk>\d+)/delete/$', views.income_delete, name='income_delete'),

]
