from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from .serializers import UserCreateSerializer, UserDisplaySerializer


# Create your views here.
User = get_user_model()


class UserViewSets(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get'], url_path='me', url_name='profile')
    def get_profile(self, request):
        serializer = UserDisplaySerializer(request.user)
        return Response(serializer.data)
