import pytest
from datetime import datetime, time, date
from rest_framework.exceptions import ValidationError
from ponto.api import serializers
from ponto.models import Funcionario, Empresa, Expediente


@pytest.mark.django_db
class TestPontoSerializer:

    def test_criar_funcionario_com_expediente(self):
        """Testa se um funcionário é criado corretamente com um expediente."""
        empresa = Empresa.objects.create(nome="Empresa Teste")

        funcionario_data = {
            'nome': 'João Silva',
            'email': 'joao@exemplo.com',
            'empresa': empresa.id,
            'expediente': {
                'inicio_expediente': '08:00:00',
                'horas_expediente': 8,
                'tempo_intervalo': 60
            }
        }

        serializer = serializers.FuncionarioCadastroSerializer(data=funcionario_data)
        assert serializer.is_valid(), serializer.errors  # Verifica se os dados são válidos
        funcionario = serializer.save()

        # Verifica se o funcionário foi criado corretamente
        assert Funcionario.objects.count() == 1
        assert Expediente.objects.count() == 1
        assert funcionario.nome == 'João Silva'
        assert funcionario.expediente.inicio_expediente == time(8, 0)
        assert funcionario.expediente.horas_expediente == 8


    def test_atualizar_funcionario_com_expediente(self):
        """Testa se um funcionário e seu expediente são atualizados corretamente."""
        empresa = Empresa.objects.create(nome="Empresa Teste")
        funcionario_data = {
            'nome': 'João Silva',
            'email': 'joao@exemplo.com',
            'empresa': empresa.id,
            'expediente': {
                'inicio_expediente': '08:00:00',
                'horas_expediente': 8,
                'tempo_intervalo': 60
            }
        }

        serializer = serializers.FuncionarioCadastroSerializer(data=funcionario_data)
        assert serializer.is_valid(), serializer.errors  # Verifica se os dados são válidos
        funcionario = serializer.save()

        updated_data = {
            'nome': 'João Silva Atualizado',
            'email': 'joao_atualizado@exemplo.com',
            'empresa': empresa.id,
            'expediente': {
                'inicio_expediente': '09:00:00',
                'horas_expediente': 9,
                'tempo_intervalo': 30
            }
        }
    
        serializer = serializers.FuncionarioCadastroSerializer(instance=funcionario, data=updated_data)
        assert serializer.is_valid(), serializer.errors
        funcionario_atualizado = serializer.save()

        # Verifica se o funcionário foi atualizado corretamente
        assert funcionario_atualizado.nome == 'João Silva Atualizado'
        assert funcionario_atualizado.email == 'joao_atualizado@exemplo.com'
        assert funcionario_atualizado.expediente.inicio_expediente == time(9,0)
        assert funcionario_atualizado.expediente.horas_expediente == 9
        assert funcionario_atualizado.expediente.tempo_intervalo == 30


    def test_validacao_campos_obrigatorios_expediente(self):
        """Testa se o serializer lança erro ao faltar dados obrigatórios do expediente."""
        empresa = Empresa.objects.create(nome="Empresa Teste")
        funcionario_data_invalido = {
            'nome': 'João Silva',
            'email': 'joao@exemplo.com',
            'empresa': empresa.id,
            'expediente': {
                'inicio_expediente': None,  # Campo obrigatório faltando
                'horas_expediente': 8,
                'tempo_intervalo': 60
            }
        }

        serializer = serializers.FuncionarioCadastroSerializer(data=funcionario_data_invalido)
        
        assert not serializer.is_valid()
        assert 'inicio_expediente' in serializer.errors['expediente']