from rest_framework.serializers import ModelSerializer
from mkapi import serializers
from mkapi.models import ProjectDD

class ProjSerialize(ModelSerializer):
    class Meta:
        model = ProjectDD
        fields = "__all__"
