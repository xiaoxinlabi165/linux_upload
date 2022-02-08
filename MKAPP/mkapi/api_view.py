from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
 
from mkapi.serializers import ProjSerialize
from mkapi.models import ProjectDD
 
 
class AuthorModelViewSet(ModelViewSet):
    queryset = ProjectDD.objects.all()
    serializer_class = ProjSerialize

class user_login(APIView):

    def post(self,request):
        parameter_json = request.body
        parameter = json.loads(parameter_json)
        print(parameter)
