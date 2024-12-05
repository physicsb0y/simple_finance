from datetime import date
from rest_framework import viewsets, filters, response, permissions, status, views
from rest_framework.decorators import action

from drf_spectacular.utils import extend_schema, OpenApiParameter

from django_filters.rest_framework import DjangoFilterBackend

from django.db.models import Sum, F, Prefetch
from django.utils.dateparse import parse_date

from apps.income.models import Expense, Income

from .models import Loan
from .serializers import FinanceReportSerializer, LoanPaymentSerializer, LoanSerializer

# Create your views here.


class LoanViwSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'loan_name': ['exact', 'icontains'],
        'status': ['exact'],
        'remaining_balance': ['gte', 'lte']
    }
    ordering_fields = ['loan_name', 'principal_amount', 'remaining_balance']

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user, is_payment=False)
    

    @extend_schema(
            request=LoanPaymentSerializer,
            responses=LoanPaymentSerializer
    )
    @action(detail=False, methods=['post'], url_path='payment', url_name='loan-payment')
    def make_payment(self, request):
        serializer = LoanPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()

        return response.Response(serializer.to_representation(payment), status=status.HTTP_201_CREATED)



class FinancialReportsDetailAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FinanceReportSerializer


    @extend_schema(
            parameters=[
                OpenApiParameter(
                    name='end_date',
                    type=date,
                    location=OpenApiParameter.QUERY,
                    description='End date for filtering (YYYY-MM-DD)'
                ),
                OpenApiParameter(
                    name='start_date',
                    type=date,
                    location=OpenApiParameter.QUERY,
                    description='Start date for filtering (YYYY-MM-DD)'
                )
            ]
    )
    def get(self, request):
        user = request.user

        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)

        if start_date:
            start_date = parse_date(start_date)
        if end_date:
            end_date = parse_date(end_date)

        serializer = self.serializer_class(
            instance=user,
            context={
                'start_date': start_date,
                'end_date': end_date
            }
        )
        return response.Response(serializer.data)
