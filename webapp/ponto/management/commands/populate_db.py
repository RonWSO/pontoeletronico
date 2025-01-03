from django.core.management.base import BaseCommand
from datetime import datetime
from ponto.models import Empresa, Funcionario, Expediente, Ponto

class Command(BaseCommand):
    help = "Cria dados falsos no banco de dados"

    def handle(self, *args, **kwargs):

        #cria manualmente objetos de model empresa
        empresas = [
            Empresa(nome="Empresa 1",endereco="endereço 1", telefone="1111111"),
            Empresa(nome="Empresa 2",endereco="endereço 2", telefone="2111111"),
            Empresa(nome="Empresa 3",endereco="endereço 3", telefone="3111111"),
            Empresa(nome="Empresa 4",endereco="endereço 4", telefone="4111111"),
            Empresa(nome="Empresa 5",endereco="endereço 5", telefone="5111111"),
            Empresa(nome="Empresa 6",endereco="endereço 6", telefone="6111111"),
        ]
        #insere no banco
        for empresa in empresas:
          try:
            print("salvando "+empresa.nome)
            empresa.save()
          except:
            print("não salvou")
            pass
        #redireciona para pegar do banco de dados
        empresas = Empresa.objects.all()

        #cria manualmente objetos de model funcionario
        funcionarios = [
            Funcionario(nome="Funcionario 1",email="exemplo1@email.com",empresa=empresas[0]),
            Funcionario(nome="Funcionario 2",email="exemplo2@email.com",empresa=empresas[1]),
            Funcionario(nome="Funcionario 3",email="exemplo3@email.com",empresa=empresas[2]),
            Funcionario(nome="Funcionario 4",email="exemplo4@email.com",empresa=empresas[3]),
            Funcionario(nome="Funcionario 5",email="exemplo5@email.com",empresa=empresas[4]),
            Funcionario(nome="Funcionario 6",email="exemplo6@email.com",empresa=empresas[5]),
            Funcionario(nome="Funcionario 7",email="exemplo7@email.com",empresa=empresas[1]),
        ]

        ##insere no banco
        
        for funcionario in funcionarios:
          print("salvando "+funcionario.nome)
          try:
            funcionario.save()
          except:
            print("não salvou")
            pass
        funcionarios = Funcionario.objects.all()

        ##cria manualmente objetos de model expediente
        expedientes = [
            Expediente(funcionario=Funcionario.objects.get(id=1),inicio_expediente='08:00',fim_expediente='17:00',tempo_intervalo=60),
            Expediente(funcionario=Funcionario.objects.get(id=2),inicio_expediente='07:00',fim_expediente='17:00',tempo_intervalo=120),
            Expediente(funcionario=Funcionario.objects.get(id=3),inicio_expediente='08:00',fim_expediente='18:00',tempo_intervalo=120),
            Expediente(funcionario=Funcionario.objects.get(id=4),inicio_expediente='09:00',fim_expediente='17:00',tempo_intervalo=60),
            Expediente(funcionario=Funcionario.objects.get(id=5),inicio_expediente='08:00',fim_expediente='19:00',tempo_intervalo=120),
            Expediente(funcionario=Funcionario.objects.get(id=6),inicio_expediente='07:00',fim_expediente='17:00',tempo_intervalo=120),
            Expediente(funcionario=Funcionario.objects.get(id=7),inicio_expediente='09:00',fim_expediente='18:00',tempo_intervalo=60),
        ]
#
        #insere no banco
        for expediente in expedientes:
          print("salvando expediente de "+ expediente.funcionario.nome)
          try:
            expediente.save()
          except:
            print("não salvou")
            pass
#
        ##cria manualmente objetos de model expediente
        #pontos = [
        #    Ponto(funcionario=funcionarios[1],data=datetime.now(),entrada_expediente="08:00:00",saida_expediente="17:00:00",inicio_intervalo="12:00:00",saida_intervalo="13:00:00"),
        #    Ponto(funcionario=funcionarios[1],data=datetime.now(),entrada_expediente="08:00:00",saida_expediente="17:00:00",inicio_intervalo="12:00:00",saida_intervalo="14:00:00"),
        #    Ponto(funcionario=funcionarios[1],data=datetime.now(),entrada_expediente="08:00:00",saida_expediente="17:00:00",inicio_intervalo="12:00:00",saida_intervalo="15:00:00"),
        #    Ponto(funcionario=funcionarios[1],data=datetime.now(),entrada_expediente="08:00:00",saida_expediente="17:00:00",inicio_intervalo="12:00:00",saida_intervalo="13:00:00"),
        #    Ponto(funcionario=funcionarios[1],data=datetime.now(),entrada_expediente="08:00:00",saida_expediente="17:00:00",inicio_intervalo="12:00:00",saida_intervalo="13:30:00"),
        #    Ponto(funcionario=funcionarios[1],data=datetime.now(),entrada_expediente="08:00:00",saida_expediente="17:00:00",inicio_intervalo="12:00:00",saida_intervalo="14:00:00"),
        #    Ponto(funcionario=funcionarios[1],data=datetime.now(),entrada_expediente="08:00:00",saida_expediente="17:00:00",inicio_intervalo="12:00:00",saida_intervalo="13:00:00"),
        #]
        #
        ##insere no banco
        #Ponto.objects.bulk_create(pontos)