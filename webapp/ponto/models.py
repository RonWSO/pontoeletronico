from django.db import models
from django.utils import timezone

class Empresa(models.Model):
    """Modelo de empresa no banco de dados"""
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, unique=True, null=False)
    endereco = models.CharField(max_length=255, null=False)
    telefone = models.CharField(max_length=255, unique=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Funcionario(models.Model):
    """Modelo de funcionário no banco de dados"""
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, null=False, db_index=True)
    email = models.EmailField(unique=True, null=False)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='funcionarios')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Expediente(models.Model):
    """Modelo de Expediente no banco de dados, horas_expediente são contadas em horas, tempo intervalo são contados em minutos"""
    id = models.AutoField(primary_key=True)
    funcionario = models.OneToOneField(Funcionario, db_index=True, on_delete=models.CASCADE, related_name='expediente')  # Alterado para OneToOneField
    inicio_expediente = models.TimeField()
    horas_expediente = models.IntegerField(default=8,null=False)
    tempo_intervalo = models.IntegerField(default=60) 

    def __str__(self):
        return f"Expediente de {self.funcionario.nome}"

class Ponto(models.Model):
    """Modelo de pontos marcados no banco de dados"""
    id = models.AutoField(primary_key=True)
    funcionario = models.ForeignKey(Funcionario, db_index=True, on_delete=models.CASCADE, related_name='ponto') 
    data = models.DateField(default=timezone.now)
    entrada_expediente = models.TimeField()
    saida_expediente = models.TimeField(blank=True, null=True) 
    inicio_intervalo = models.TimeField(blank=True, null=True)
    saida_intervalo = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"Ponto de {self.funcionario.nome} em {self.data}"

class Usuario(models.Model):
    """Modelo de usuários no banco de dados"""
    id = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=255, unique=True)
    senha = models.CharField(max_length=255) 

    def __str__(self):
        return self.usuario