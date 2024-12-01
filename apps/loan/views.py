from rest_framework import viewsets, filters, response, permissions

from django_filters.rest_framework import DjangoFilterBackend

from .models import Loan
from .serializers import LoanSerializer

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
