from rest_framework import serializers

from .models import Loan


class LoanSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = Loan
        fields = ['id', 'loan_name', 'principal_amount', 'interest_rate', 'tenure_months', 'monthly_installment', 'remaining_balance', 'status', 'notes']
        read_only_fields = ['id', 'monthly_installment', 'remaining_balance', 'status']
