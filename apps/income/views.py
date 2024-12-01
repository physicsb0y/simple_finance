import hashlib, json

from rest_framework import viewsets, permissions, filters, response

from django_filters.rest_framework import DjangoFilterBackend

from django.core.cache import cache

from .models import Expense, Income
from .serializers import ExpenseSerializer, IncomeSerializer

# Create your views here.


class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'status': ['exact'],
        'date_received': ['exact', 'gte', 'lte'],
        'source_name': ['exact', 'icontains']
    }
    ordering_fields = ['amount', 'date_received', 'source_name']

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    def perform_create(self, serializer):
        self._invalidate_cache(self.request)
        return serializer.save(user=self.request.user)
    

    def _generate_cache_key(self, request):
        query_params = request.query_params.dict()
        query_params['user_id'] = request.user.id

        params_string = json.dumps(query_params, sort_keys=True)
        cache_key = f"income_list:user_{request.user.id}:{hashlib.sha256(params_string.encode()).hexdigest()}"

        tracker_key = f"income_cache_keys_user_{request.user.id}"
        tracked_keys = cache.get(tracker_key, set())
        tracked_keys.add(cache_key)
        cache.set(tracker_key, tracked_keys, timeout=3600)

        return cache_key
    
    def list(self, request, *args, **kwargs):
        cache_key = self._generate_cache_key(request)

        cached_data = cache.get(cache_key)
        if cached_data is not None:
            print("from cached data")
            return response.Response(cached_data)
        
        resp = super().list(request, *args, **kwargs)
        cache.set(cache_key, resp.data, timeout=3600)
        return resp
    
    def _invalidate_cache(self, request):
        tracker_key = f"income_cache_keys_user_{request.user.id}"
        tracked_keys = cache.get(tracker_key, set())
    
        if tracked_keys:
            print("invalidated keys : ", tracked_keys, tracker_key)
            cache.delete_many(tracked_keys)
            cache.delete(tracker_key)

    def perform_update(self, serializer):
        self._invalidate_cache(self.request)
        return super().perform_update(serializer)


    def perform_destroy(self, instance):
        self._invalidate_cache(self.request)
        return super().perform_destroy(instance)




class ExpenseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'category': ['exact'],
        'due_date': ['exact', 'gte', 'lte'],
        'status': ['exact']
    }
    ordering_fields = ['amount', 'due_date']
