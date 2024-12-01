from django.db import models
from apps.utils.abstract_model import TimeStampModel
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


class STATUSCHOICES(models.TextChoices):
    PENDING = 'P', 'Pending'
    RECEIVED = 'R', 'Received'



class Income(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    date_received = models.DateField()
    status = models.CharField(max_length=1, choices=STATUSCHOICES.choices, default=STATUSCHOICES.PENDING)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.source_name} - {self.amount}"
    
    class Meta:
        verbose_name = "Income"
        verbose_name_plural = "Incomes"



class ExpenseCategory(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Expense Category"
        verbose_name_plural = "Expense Categories"



class Expense(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=1, choices=STATUSCHOICES.choices, default=STATUSCHOICES.PENDING)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.category} - {self.amount}"

    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"
