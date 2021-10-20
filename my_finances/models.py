from django.db import models
from django.contrib.auth.models import User

from datetime import datetime


# Create your models here.

class Income(models.Model):
    class IncomeTypes(models.IntegerChoices):
        SALARY = 1, "SALARY"
        BONUS = 2, "BONUS"
        GIFT = 3, "GIFT"
        OTHER = 4, "OTHER"

    class RepetitiveInterval(models.IntegerChoices):
        NA = 1, 'N/A'
        DAYS = 2, "DAYS"
        WEEKS = 3, "WEEKS"
        MONTHS = 4, "MONTHS"
        YEARS = 5, "YEARS"


    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incomes')
    value = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    type = models.PositiveSmallIntegerField(choices=IncomeTypes.choices)
    repetitive = models.BooleanField(default=False)
    repetition_interval = models.PositiveSmallIntegerField(choices=RepetitiveInterval.choices, default=1)
    repetition_time = models.PositiveSmallIntegerField(default=0)
    comment = models.TextField(max_length=1024, null=True, blank=True)
    update_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Income {self.id} - {self.type} - {self.date.strftime("%Y/%d/%d")}'

    class Meta:
        verbose_name_plural = 'incomes'


class Outcome(models.Model):
    class OutcomeTypes(models.IntegerChoices):
        RENT = 1, "RENT"
        BILLS = 2, "BILLS"
        CAR = 3, "CAR"
        TRAVEL = 4, "TRAVEL"
        HEALTH = 5, "HEALTH"
        GROCERIES = 6, "GROCERIES"
        FUN = 7, "FUN"
        CLOTHES = 8, "CLOTHES"
        CHARITY = 9, "CHARITY"

    class RepetitiveInterval(models.IntegerChoices):
        NA = 1, 'N/A'
        DAYS = 2, "DAYS"
        WEEKS = 3, "WEEKS"
        MONTHS = 4, "MONTHS"
        YEARS = 5, "YEARS"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outcomes')
    value = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    type = models.PositiveSmallIntegerField(choices=OutcomeTypes.choices)
    repetitive = models.BooleanField(default=False)
    repetition_interval = models.PositiveSmallIntegerField(choices=RepetitiveInterval.choices, default=1)
    repetition_time = models.PositiveSmallIntegerField(default=0)
    comment = models.TextField(max_length=1024, null=True, blank=True)
    update_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Outcome {self.id} - {self.type} - {self.date.strftime("%Y/%d/%d")}'

    class Meta:
        verbose_name_plural = 'outcomes'

class Balance(models.Model):
    class BalanceType(models.IntegerChoices):
        CURRENT = 1, "CURRENT"
        SAVINGS = 2, "SAVINGS"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='balances')
    value = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.PositiveSmallIntegerField(choices=BalanceType.choices)
    date = models.DateField()
    comment = models.TextField(max_length=1024, null=True, blank=True)
    update_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Balance {self.id} - {self.type}'

    class Meta:
        verbose_name_plural = 'balances'

