from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from rest_framework import serializers
from datetime import datetime
from ponto import models
import logging
import re

class EmpresaSerializer(serializers.ModelSerializer):
    """Serializa os dados comuns de empresa para retorno básico com informações de nome, endereço, telefone."""
    class Meta:
        model = models.Empresa
        fields = (
            'id',
            'nome',
            'endereco',
            'telefone'
        )
    def validate_telefone(self, value):
        """Valida se o telefone foi inserido com algo além de numeros"""
        if bool(re.search(r'[^0-9]',value)):
            raise serializers.ValidationError("Há não caracteres que não são números no telefone.")
        return value

    def validate_nome(self, value):
        """Remove espaços em branco antes e depois do primeiro caractere do nome"""
        return value.strip()

    def validate_endereco(self, value):
        """Remove espaços em branco antes e depois do primeiro caractere do endereço"""
        return value.strip()

class FuncionarioSerializer(serializers.ModelSerializer):
    """Serializa os dados comuns de funcionario para retorno básico com informações de nome, email, empresa relacionada."""
    empresa = serializers.PrimaryKeyRelatedField(queryset=models.Empresa.objects.all())
    
    class Meta:
        model = models.Funcionario
        fields = (
            'id',
            'nome',
            'email',
            'empresa',
        )
        
    def validate_email(self,value):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.match(regex, value):
            raise serializers.ValidationError('Endereço de e-mail inválido.')
        return value
    
class ExpedienteSerializer(serializers.ModelSerializer):
    """Serializa os dados de expediente de funcionário para retorno básico com informações de funcionario, inicio_expediente, horas_trabalhadas, tempo de intervalo."""
    funcionario = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = models.Expediente
        fields = (
            'funcionario',
            'inicio_expediente',
            'horas_expediente',
            'tempo_intervalo'
        )
    def validate_horas_expediente(self,value):
        if value < 4:
            raise serializers.ValidationError({'horas_expediente':'Minimo de horas inválido.'})
        return value
    def validate_tempo_intervalo(self,value):
        if value < 20:
            raise serializers.ValidationError({'tempo_intervalo':'Minimo de minutos de intervalo inválido.'})
        return value

class PontoSerializer(serializers.ModelSerializer):
    """Serializa os dados de pontos."""
    data = serializers.DateField(format="%Y-%m-%d")
    funcionario_id = serializers.IntegerField(write_only=True)
    funcionario = serializers.StringRelatedField()

    class Meta:
        model = models.Ponto
        fields = (
            'funcionario_id',
            'funcionario',
            'data',
            'entrada_expediente',
            'saida_expediente',
            'inicio_intervalo',
            'saida_intervalo'
        )

    def create(self, validated_data):
        """Cria o ponto"""
        funcionario_id = validated_data.pop('funcionario_id')
        funcionario = models.Funcionario.objects.get(id=funcionario_id)
        ponto = models.Ponto.objects.create(funcionario=funcionario, **validated_data)
        return ponto
    
    def to_representation(self, instance):
        """Instancia que modifica a data para a representação"""
        data = super().to_representation(instance)
        try:
            date_obj = datetime.strptime(data['data'], "%Y-%m-%d")
            data['data'] = date_obj.strftime("%d/%m/%Y")
        except ValueError:
            raise serializers.ValidationError({'modelo_data':'Data não está registrada no banco com o formato padrão'}) 
        return data

    def validate(self, obj):
        if obj['saida_expediente'] < obj['entrada_expediente']:
            raise serializers.ValidationError({'saida_expediente': 'Saída do expediente não pode ser anterior à entrada.'})
        if obj['saida_intervalo'] < obj['inicio_intervalo']:
            raise serializers.ValidationError({'saida_intervalo': 'Saída do intervalo não pode ser anterior à saída do expediente.'})
        return obj
    
class EmpresaDetalhesLista(serializers.ModelSerializer):
    quantidade_funcionarios = serializers.SerializerMethodField()

    class Meta:
        model = models.Empresa
        fields = ('id', 'nome', 'endereco', 'telefone', 'quantidade_funcionarios')

    def get_quantidade_funcionarios(self, obj):
        return obj.funcionarios.count()
    
class FuncionarioDetalhesCompletoSerializer(serializers.ModelSerializer):
    expediente = ExpedienteSerializer()
    empresa = serializers.PrimaryKeyRelatedField(queryset=models.Empresa.objects.all())

    class Meta:
        model = models.Funcionario
        fields = ('id', 'nome', 'email', 'empresa', 'expediente')

class FuncionarioCadastroSerializer(serializers.ModelSerializer):
    expediente = ExpedienteSerializer()
    empresa = serializers.PrimaryKeyRelatedField(queryset=models.Empresa.objects.all())

    class Meta:
        model = models.Funcionario
        fields = ('id', 'nome', 'email', 'empresa', 'expediente')

    def create(self, validated_data):
        expediente_data = validated_data.pop('expediente')
        funcionario = models.Funcionario.objects.create(**validated_data)
        
        # Criar o expediente relacionado ao funcionário
        models.Expediente.objects.create(funcionario=funcionario, **expediente_data)
        
        return funcionario
    
    def update(self, instance, validated_data):
        # Extrair dados do expediente do validated_data
        expediente_data = validated_data.pop('expediente', None)

        # Atualizar dados do funcionário
        instance.nome = validated_data.get('nome', instance.nome)
        instance.email = validated_data.get('email', instance.email)
        instance.empresa = validated_data.get('empresa', instance.empresa)
        instance.save()

        # Se houver dados de expediente, atualizar o expediente relacionado
        if expediente_data:
            expediente_instance = instance.expediente  # Obter o expediente do funcionário

            inicio_expediente = expediente_data.get('inicio_expediente')
            if inicio_expediente is not None:
                expediente_instance.inicio_expediente = inicio_expediente
            else:
                raise serializers.ValidationError({'inicio_expediente': 'Este campo é obrigatório e não pode ser nulo.'})
            
            horas_expediente = expediente_data.get('horas_expediente')
            if horas_expediente is not None:
                expediente_instance.horas_expediente = horas_expediente
            else:
                raise serializers.ValidationError({'horas_expediente': 'Este campo é obrigatório e não pode ser nulo.'})
            
            tempo_intervalo = expediente_data.get('tempo_intervalo')
            if tempo_intervalo is not None:
                expediente_instance.tempo_intervalo = tempo_intervalo
            else:
                raise serializers.ValidationError({'tempo_intervalo': 'Este campo é obrigatório e não pode ser nulo.'})
            
            expediente_instance.save()
        return instance