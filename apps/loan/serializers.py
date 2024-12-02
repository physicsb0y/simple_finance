from datetime import date

from rest_framework import serializers

from django.db.models import Sum, Prefetch, F

from apps.income.models import Expense, Income

from .models import Loan


class LoanSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = Loan
        fields = ['id', 'user', 'loan_name', 'principal_amount', 'interest_rate', 'tenure_months', 'monthly_installment', 'remaining_balance', 'status', 'notes']
        read_only_fields = ['id', 'user', 'monthly_installment', 'remaining_balance', 'status']



class LoanPaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'loan_payment_date', 'loan_payment_amount', 'notes', 'is_payment']



class LoanPaymentSerializer(serializers.Serializer):
    loan_id = serializers.PrimaryKeyRelatedField(queryset=Loan.objects.all())
    payment_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    payment_date = serializers.DateField(default=date.today)
    notes = serializers.CharField(max_length=255, required=False)

    def validate(self, data):
        loan = data['loan_id']
        payment_amount = data['payment_amount']

        if payment_amount <= 0:
            raise serializers.ValidationError("Payment amount must be greater than zero.")
        
        if loan.remaining_balance <= 0:
            raise serializers.ValidationError("This loan is already fully paid.")
        
        if payment_amount > loan.remaining_balance:
            raise serializers.ValidationError("Payment amount exceeds the remaining balance.")
        return super().validate(data)
    
    def create(self, validated_data):
        loan = validated_data['loan_id']
        payment_amount = validated_data['payment_amount']
        payment_date = validated_data['payment_date']
        notes = validated_data.get('notes', None)

        loan.remaining_balance -= payment_amount
        if loan.remaining_balance <= 0:
            loan.status = Loan.LOAN_STATUS.PAID

        loan.save()

        payment = Loan.objects.create(
            user=loan.user,
            loan_name=loan.loan_name,
            principal_amount=loan.principal_amount,
            interest_rate=loan.interest_rate,
            tenure_months=loan.tenure_months,
            monthly_installment=loan.monthly_installment,
            remaining_balance=loan.remaining_balance,
            status=loan.status,
            notes=notes,
            loan=loan,
            loan_payment_date=payment_date,
            loan_payment_amount=payment_amount,
            is_payment=True
        )

        return payment
    

    def to_representation(self, instance):
        loan = instance.loan
        related_payments = Loan.objects.filter(loan=loan, is_payment=True)
        payments_data = LoanPaymentDetailSerializer(related_payments, many=True).data

        return {
            "message": "Payment recorded successfully.",
            "payment": LoanSerializer(loan).data,
            "related_payments": payments_data
        }




class FinanceReportSerializer(serializers.Serializer):
    total_income = serializers.DecimalField(max_digits=20, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=20, decimal_places=2)
    total_expense_trend = serializers.ListField()
    income_trend = serializers.ListField()
    total_loan_trend = serializers.ListField()


    def to_representation(self, instance):
        user = instance
        incomes = Income.objects.filter(
                user=user
            ).values(
                'source_name', 
                'amount', 
                'date_received', 
                'status', 
                'notes'
            )
        total_income = sum(income['amount'] for income in incomes) if incomes else 0

        expenses = Expense.objects.filter(
            user=user
        ).values(
            'category__name',
            'amount',
            'due_date',
            'status',
            'notes'
        )
        total_expenses = sum(expense['amount'] for expense in expenses) if expenses else 0

        loans = Loan.objects.filter(
            user=user,
            is_payment=False
        ).prefetch_related(
            Prefetch(
                'loan_payments',
                queryset=Loan.objects.filter(is_payment=True).only(
                    'loan',
                    'loan_payment_date',
                    'loan_payment_amount',
                    'notes'
                )
            )
        )

        total_loan_trend = [
            {
                'loan_name': loan.loan_name,
                'principal_amount': loan.principal_amount,
                'interest_rate': loan.interest_rate,
                'tenure_months': loan.tenure_months,
                'monthly_installment': loan.monthly_installment,
                'remaining_balance': loan.remaining_balance,
                'status': loan.status,
                'notes': loan.notes,
                'installments': list(
                    loan.loan_payments.values(
                        'loan_payment_date',
                        'loan_payment_amount',
                        'notes'
                    )
                )
            }
            for loan in loans
        ]

        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'total_expense_trend': expenses,
            'income_trend': incomes,
            'total_loan_trend': total_loan_trend
        }
