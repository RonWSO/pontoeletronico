from rest_framework import viewsets
from . import serializers
from ponto import models

class EmpresaViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EmpresaSerializer
    queryset = models.Empresa.objects.all()