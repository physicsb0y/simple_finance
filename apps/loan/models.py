from decimal import Decimal, getcontext, ROUND_HALF_UP  


from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from apps.utils.abstract_model import TimeStampModel
# Create your models here.


User = get_user_model()


class Loan(TimeStampModel):
    class LOAN_STATUS(models.TextChoices):
        ACTIVE = 'A', 'Active'
        PAID = 'P', 'Paid'


    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_loans')
    loan_name = models.CharField(max_length=255)
    principal_amount = models.DecimalField(max_digits=15, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    tenure_months = models.PositiveIntegerField()
    monthly_installment = models.DecimalField(max_digits=15, decimal_places=2)
    remaining_balance = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=1, choices=LOAN_STATUS.choices, default=LOAN_STATUS.ACTIVE)
    notes = models.TextField(null=True, blank=True)

    ##for loan payments
    loan = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='loan_payments')
    loan_payment_date = models.DateField(null=True, blank=True)
    loan_payment_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    is_payment = models.BooleanField(default=False, null=True)


    def __str__(self):
        return f"{self.loan_name} - {self.principal_amount}"
    
    def calculate_monthly_installment(self):
        if self.interest_rate == 0:
            emi = self.principal_amount / self.tenure_months

        else:
            getcontext().prec = 15
            p = Decimal(self.principal_amount)
            annual_rate = Decimal(self.interest_rate)
            n = self.tenure_months
            r = annual_rate / Decimal(12 * 100)

            emi =  p * r * ((1 +r ) ** n) / (((1 + r) ** n) - 1)

        return emi.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.remaining_balance = self.principal_amount

        self.monthly_installment = self.calculate_monthly_installment()

        if self.remaining_balance < Decimal(0):
            self.status = self.LOAN_STATUS.PAID
        else:
            self.status = self.LOAN_STATUS.ACTIVE


        self.full_clean()
        return super().save(*args, **kwargs)
    
    def clean(self):
        clean = super().clean()
        if self.principal_amount <= 0:
            raise ValidationError("Principal amount must be greater than zero.")
        
        if self.interest_rate < 0:
            raise ValidationError("Interest rate can't be negative.")
        
        if self.tenure_months <= 0:
            raise ValidationError("Tenure in months must be greater than zero.")
        
        return clean
