from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from django.http import HttpResponse
from .api import serializers
from . import models
from . import forms
import fitz
from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

class LoginView(LoginView):
    template_name = 'login.html'
    authentication_form = LoginForm

    def get_success_url(self):
        return '/gerenciamento/'

@login_required(login_url='/login/')
@api_view(['GET','POST'])
def Empresas(request):
    """Função que busca as empresas ou cadastra uma nova"""
    if request.method =='GET':
        empresas = models.Empresa.objects.all()
        nome = request.GET.get('nome')
        if nome:
            empresas = empresas.filter(nome__icontains=nome)
        serializer = serializers.EmpresaSerializer(empresas, many=True)
        return Response(serializer.data)
    
    if request.method =='POST':
        serializer = serializers.EmpresaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Empresa cadastrada com sucesso!"}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@login_required(login_url='/login/')
@api_view(['GET','DELETE','PUT'])
def EmpresaDetalhe(request,id):
    """Função que busca informação detalhada da empresa, deleta ou atualiza."""
    try:
        empresa = models.Empresa.objects.get(pk=id)
    except models.Empresa.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method =='GET':
        empresa = get_object_or_404(models.Empresa, pk=id)
        serializer = serializers.EmpresaSerializer(empresa)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = serializers.EmpresaSerializer(empresa, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Empresa atualizada com sucesso!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        try:
            empresa.delete()
            return Response({"success": True, "message": "Empresa excluída com sucesso!"},status=status.HTTP_200_OK)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required(login_url='/login/')  
@api_view(['GET','POST'])
def Funcionarios(request):
    """Função que busca os funcionário ou cadastra um novo"""
    if request.method =='GET':
        funcionarios = models.Funcionario.objects.all()
        serializer = serializers.FuncionarioDetalhesCompletoSerializer(funcionarios, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
    # Extrair os dados do request e passar para o serializer
        serializer = serializers.FuncionarioCadastroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Funcionário cadastrado com sucesso!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@login_required(login_url='/login/')
@api_view(['GET','DELETE','PUT'])
def FuncionarioDetalhe(request,id):
    """Função que busca informação detalhada do funcionário, deleta ou atualiza."""
    try:
        funcionario = models.Funcionario.objects.get(pk=id)
    except models.Funcionario.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method =='GET':
        funcionario = get_object_or_404(models.Funcionario, pk=id)
        serializer = serializers.FuncionarioSerializer(funcionario)
        return Response(serializer.data)

    if request.method =='DELETE':
        try:
            funcionario.delete()
            return Response({"success": True, "message": "Funcionário excluído com sucesso!"},status=status.HTTP_200_OK)
        except funcionario.DoesNotExist:
            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    if request.method =='PUT':
        serializer = serializers.FuncionarioCadastroSerializer(funcionario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Funcionario atualizado com sucesso!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required(login_url='/login/')
@api_view(['GET','POST','DELETE'])
def FuncionarioExpediente(request,id):
    """Função para buscar, cadastrar, atualizar ou deletar o expediente cadastrado para o funcionário"""
    if request.method =='GET':
        try:
            funcionario = get_object_or_404(models.Funcionario, pk=id)
            expediente = get_object_or_404(models.Expediente, funcionario=funcionario)
            serializer = serializers.ExpedienteSerializer(expediente)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    if request.method =='POST':
        serializer = serializers.ExpedienteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        return Response(serializer.errors, status=400)

@login_required(login_url='/login/')
@api_view(['GET','POST'])
def FuncionarioPonto(request,id):
    """Função para buscar, cadastrar ou alterar o ponto do funcionário"""
    if request.method == 'GET':
        try:
            funcionario = get_object_or_404(models.Funcionario, pk=id)
            pontos = models.Ponto.objects.filter(funcionario=funcionario)  # Filtra todos os pontos do funcionário
            serializer = serializers.PontoSerializer(pontos, many=True)
            return Response(serializer.data)
        except models.Funcionario.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        serializer = serializers.PontoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Funcionario atualizado com sucesso!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@login_required(login_url='/login/')
@api_view(['GET'])
def relatorio(request,id):
    """Função que faz o download do pdf de relatório"""
    funcionario = models.Funcionario.objects.get(id=id)
    pontos = models.Ponto.objects.filter(funcionario=funcionario).order_by('data')
    doc = gerar_relatorio_ponto(funcionario,pontos)
    # Abrir o arquivo PDF em modo binário e ler o conteúdo
    with open(f"relatorio_ponto_{funcionario.nome}.pdf", "rb") as pdf:
        pdf_data = pdf.read()

    # Criar a resposta HTTP
    response = HttpResponse(pdf_data, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_ponto_{}.pdf"'.format(funcionario.nome)

    return response
@login_required(login_url='/login/')
def mainPage(request):
    """Retorna a página principal"""
    return redirect('/gerenciamento')

@login_required(login_url='/login/')
def gerenciamento(request):
    """Função que renderiza a página de gerenciamento"""
    empresas = models.Empresa.objects.all().order_by('nome')
    
    nome = request.GET.get('nome')
    if nome:
        empresas = empresas.filter(nome__icontains=nome)
    
    paginator = Paginator(empresas, 10)
    page = request.GET.get('page')
    
    try:
        empresas_page = paginator.page(page)
    except PageNotAnInteger:
        empresas_page = paginator.page(1)
    except EmptyPage:
        empresas_page = paginator.page(paginator.num_pages)

    serializer = serializers.EmpresaDetalhesLista(empresas_page, many=True)

    context = {
        'empresas': serializer.data,
        'paginator': paginator,
        'page_obj': empresas_page,
    }
    return render(request, 'gerenciamento.html', context)

@login_required(login_url='/login/')
def empresa(request,empresa_id):
    """Página para gerenciamento da empresa, permite criar, atualizar e excluir funcionários"""
    try:
        empresa = models.Empresa.objects.get(id=empresa_id)
        nome = request.GET.get('nome')
        if empresa:
            empresa_serializer = serializers.EmpresaSerializer(empresa)
            funcionarios = models.Funcionario.objects.filter(empresa=empresa).order_by('nome')
            if funcionarios:
                if nome:
                    funcionarios = funcionarios.filter(nome__icontains=nome)
                
                paginator = Paginator(funcionarios, 10)
                page = request.GET.get('page')
                try:
                    funcionario_page = paginator.page(page)
                except PageNotAnInteger:
                    funcionario_page = paginator.page(1)
                except EmptyPage:
                    funcionario_page = paginator.page(paginator.num_pages)

                funcionarios_serializer = serializers.FuncionarioCadastroSerializer(funcionarios, many=True)

                context  = {
                    "funcionarios":funcionarios_serializer.data,
                    "empresa":empresa_serializer.data,
                    'paginator': paginator,
                    'page_obj': funcionario_page,
                }
            else:
                context  = {
                    "empresa":empresa_serializer.data
                }
    except:
        context = {
            "error":"Não foi encontrada nenhuma empresa"
        }
        return render(request, '404.html', context)
    return render(request, 'empresa.html', context)

@login_required(login_url='/login/')
def funcionario(request,funcionario_id):
    """função que renderiza a página de funcionários"""
    try:
        # Buscar o funcionário
        funcionario = get_object_or_404(models.Funcionario, id=funcionario_id)
    
        # Buscar os pontos relacionados ao funcionário
        pontos = models.Ponto.objects.filter(funcionario=funcionario)
        
        # Serializar o funcionário
        serializer_funcionario = serializers.FuncionarioDetalhesCompletoSerializer(funcionario)
        
        # Serializar os pontos
        serializer_pontos = serializers.PontoSerializer(pontos, many=True)
        # Construir o contexto com os dados serializados
        context = {
            'funcionario': serializer_funcionario.data,
            'pontos': serializer_pontos.data,
        }
        return render(request, 'funcionario.html', context)
    except:
        context = {
            "error":"Não foi encontrada nenhuma empresa"
        }
    return render(request, '404.html', context)

@login_required(login_url='/login/')   
def pontos_funcionarios(request, empresa_id):
    """Exibe a tabela de pontos filtrada por data e nome do funcionário"""
    try:
        empresa = models.Empresa.objects.get(id=empresa_id)
        pontos = models.Ponto.objects.filter(funcionario__empresa=empresa).order_by('data')

        nome = request.GET.get('nome')
        data_inicio = request.GET.get('data_inicio')
        data_fim = request.GET.get('data_fim')

        if nome:
            pontos = pontos.filter(funcionario__nome__icontains=nome)
        if data_inicio and data_fim:
            pontos = pontos.filter(data__range=[data_inicio, data_fim])


        paginator = Paginator(pontos, 10)
        page = request.GET.get('page')
        try:
            ponto_page = paginator.page(page)
        except PageNotAnInteger:
            ponto_page = paginator.page(1)
        except EmptyPage:
            ponto_page = paginator.page(paginator.num_pages)

        pontos_serializer = serializers.PontoSerializer(ponto_page, many=True)

        context = {
            "pontos": pontos_serializer.data,
            "empresa": empresa,
            'paginator': paginator,
            'page_obj': ponto_page,
        }
    except models.Empresa.DoesNotExist:
        context = {"error": "Empresa não encontrada"}

    return render(request, 'ponto.html', context)

@login_required(login_url='/login/')
def calcular_horas(ponto, expediente):
    """Calcula as horas de trabalho, atrasos e horas extras"""
    horas_trabalhadas = datetime.combine(ponto.data, ponto.saida_expediente) - datetime.combine(ponto.data, ponto.entrada_expediente)
    horas_esperadas = timedelta(hours=expediente.horas_expediente, minutes=expediente.tempo_intervalo)
    
    # Calculando atrasos e horas extras
    atraso = timedelta(0)
    horas_extras = timedelta(0)
    if ponto.entrada_expediente > expediente.inicio_expediente:
        atraso = datetime.combine(ponto.data, ponto.entrada_expediente) - datetime.combine(ponto.data, expediente.inicio_expediente)
    if horas_trabalhadas > horas_esperadas:
        horas_extras = horas_trabalhadas - horas_esperadas
    
    return horas_trabalhadas, atraso, horas_extras, horas_esperadas

@login_required(login_url='/login/')
def calcular_faltas(funcionario, data_inicio, data_fim):
    """Calcula a quantidade de faltas (dias úteis em que o funcionário não marcou ponto)."""
    # Obtém todas as datas de ponto do funcionário
    pontos = models.Ponto.objects.filter(funcionario=funcionario, data__range=(data_inicio, data_fim)).values_list('data', flat=True)
    pontos_registrados = set(pontos)  # Datas em que o ponto foi registrado

    dias_uteis = []
    data_atual = data_inicio

    # Itera sobre o intervalo de datas
    while data_atual <= data_fim:
        # Considera apenas dias úteis (exclui finais de semana)
        if data_atual.weekday() < 5:  # 0 = segunda-feira, 4 = sexta-feira
            dias_uteis.append(data_atual)
        data_atual += timedelta(days=1)

    # Calcula as faltas comparando dias úteis com os dias que o funcionário registrou ponto
    faltas = [dia for dia in dias_uteis if dia not in pontos_registrados]
    
    # Retorna a quantidade de faltas
    return len(faltas)

@login_required(login_url='/login/')
def gerar_relatorio_ponto(funcionario, pontos):
    """Produz o pdf do relatório"""
    doc = fitz.open()
    page = doc.new_page()
    faltas = 0
    qtd_atraso = 0
    if len(pontos)>0:
        data_inicio = pontos[0].data
        data_fim = datetime.now()
        # Calcula faltas
        faltas = calcular_faltas(funcionario, data_inicio, data_fim.date())

    # Cabeçalho
    titulo = f"Relatório de Batidas de Ponto - {funcionario.nome}"
    page.insert_text((50, 50), titulo, fontsize=14)

    y = 100  # posição vertical inicial para texto
    
    
    
    y += 40
    page.insert_text((50, y), "Data         |  \tEntrada     |  \tSaída     |  \tAtraso     |  \tHoras Trabalhadas     |  \tHoras Extras", fontsize=12)
    
    y += 20

    for ponto in pontos:
        expediente = ponto.funcionario.expediente
        horas_trabalhadas, atraso, horas_extras, horas_esperadas = calcular_horas(ponto, expediente)
        if horas_trabalhadas.total_seconds() < horas_esperadas.total_seconds() / 2:
            faltas = faltas+1
        if horas_trabalhadas <= timedelta(0):
            continue
        if atraso.total_seconds() / 60 > 5:
            qtd_atraso = qtd_atraso+1
        line = f"{ponto.data}      \t{ponto.entrada_expediente}         \t{ponto.saida_expediente}        \t{atraso}                        \t{horas_trabalhadas}                         \t{horas_extras}"
        page.insert_text((50, y), line, fontsize=10)
        y += 20

    page.insert_text((50,100),f"Quantidade de Faltas: {faltas}")
    page.insert_text((50,120),f"Quantidade de Atrasos: {qtd_atraso}")

    # Salvar o PDF
    doc.save(f"relatorio_ponto_{funcionario.nome}.pdf")
    doc.close()

    return doc