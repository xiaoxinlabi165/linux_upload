from django.contrib.auth.models import User, Group
from . models import ProjectDD
from rest_framework import viewsets
from . serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API 允许查看或编辑用户
    """
    queryset = ProjectDD.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
