from django.test import TestCase

# Create your tests here.
from mkapi.serializers import ProjSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class DeviceReport(APIView):
    """
    上报信息, 无需鉴权
    """
       authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        serializer = ProjSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

