from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('',views.mainPage),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('empresa/',views.Empresas, name="empresa"),
    path('empresa/<int:id>',views.EmpresaDetalhe),
    path('funcionario/',views.Funcionarios),
    path('funcionario/<int:id>',views.FuncionarioDetalhe),
    path('funcionario/<int:id>/expediente',views.FuncionarioExpediente),
    path('funcionario/<int:id>/ponto',views.FuncionarioPonto),
    path('gerenciamento/',views.gerenciamento, name="gerenciamento"),
    path('gerenciamento/empresa/<int:empresa_id>/',views.empresa, name="detalhe_empresa"),
    path('gerenciamento/empresa/funcionario/<int:funcionario_id>/',views.funcionario, name="detalhe_funcionário"),
    path('funcionario/<int:id>/relatorio',views.relatorio, name="gerarRelatorio"),
    path('gerenciamento/empresa/<int:empresa_id>/ponto',views.pontos_funcionarios, name="pontos_empresa"),
]
