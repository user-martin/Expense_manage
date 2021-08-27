from django.db import models
from django.urls import reverse



class Expense(models.Model):
    Payment_Choices = (
        ('Online', 'Online'),
        ('Cash', 'Cash'),
        ('Credit Card','Credit Card')
    )
    date = models.DateField()
    description = models.CharField(max_length=1000, null=True)
    type = models.CharField(max_length=30)
    payment = models.CharField(max_length=30, choices=Payment_Choices)
    amount = models.FloatField()
    created_by = models.CharField(max_length=100)
    created_at = models.DateField()

    class Meta:
        verbose_name = 'Expense'
        verbose_name_plural = 'Expenses'
        ordering = ['-id']


class Income(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=1000, null=True)
    amount = models.FloatField()
    created_by = models.CharField(max_length=100)
    created_at = models.DateField()

    class Meta:
        verbose_name = 'Income'
        verbose_name_plural = 'Incomes'
        ordering = ['-id']
