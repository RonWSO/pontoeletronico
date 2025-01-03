# Ponto Eletrônico

Um sistema que permite cadastrar empresas, cadastrar funcionários junto a elas, cadastrar as batidas de pontos desses funcionários e gerar relatórios de cada funcionário.

Utilizando python, django, djangorestframework, mysql

# Necessário
Instalar docker no computador
link: https://docs.docker.com/engine/install/

# Instalação
# Passo 1
    Entre na pasta db, no arquivo .env coloque as informações do seu usuário de db, senha do root, nome do banco de dados.

# Passo 2
    Entre na pasta webapp, no arquivo .env coloque as informações de usuário do db, crie as informações de admin do django.
    As informações de login do admin do django serão necessárias para entrar na aplicação.

# Passo 3
    Volte a raiz do projeto e rode o comando.

    docker compose up --build -d

    Espere a instalação terminar.

# Passo 4
    A aplicação estará rodando no localhost/
    Use as informações do .env dentro de webapp para poder logar no sistema login = SUPERADMINDJANGO e a senha = SUPERSENHADJANGO

# Passo 5
    No sistema é possível cadastrar e editar empresas. Acessando as informações da empresa ao clicar no nome dela dentro da tabela é possível cadastrar, excluir e atualizar funcionários ligados a ela; Marcar batidas de ponto e tirar relatórios por cada funcionário.

