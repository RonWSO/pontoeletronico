document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('formulario_empresa');
    const form_exclusao = document.getElementById('form_exclusao_empresa');
    const salvarBtn = document.getElementById('btn_salvar_empresa');
    const excluirBtn = document.getElementById('btn_excluir_empresa');

    salvarBtn.addEventListener('click', function (event) {
        event.preventDefault();
        const successAlert = document.querySelector('.alert-success');
        const errorAlert = document.querySelector('.alert-danger');
        const errorList = errorAlert.querySelector('ul');
        
        // Pegando os valores do formulário
        const nome = form.elements['nome_empresa'].value;
        const endereco = form.elements['endereco_empresa'].value;
        const telefone = $('.telefone_empresa').cleanVal();
        const id_empresa = form.elements['id_empresa'].value;
        
        const method = id_empresa ? 'PUT' : 'POST';
        const url = id_empresa ? `/empresa/${id_empresa}` : '/empresa/';

        // Dados a serem enviados
        const data = {
            nome,
            endereco,
            telefone
        };
        
        if (method === 'PUT') {
            data.id = id_empresa;
        }

        // Converte os dados para JSON
        const body = JSON.stringify(data);

        try {
            // Fazendo a requisição AJAX
            fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: body
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Erro na resposta da requisição");
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    successAlert.style.display = 'block';
                    errorAlert.style.display = 'none';
                    form.reset(); // Limpa os campos do formulário
                } else {
                    errorAlert.style.display = 'block';
                    errorList.innerHTML = ''; // Limpa a lista de erros

                    // Tratando possíveis erros do backend
                    if (data.nome) {
                        const li = document.createElement('li');
                        li.textContent = data.nome;
                        errorList.appendChild(li);
                    } 
                    if (data.telefone) {
                        const li = document.createElement('li');
                        li.textContent = data.errors;
                        errorList.appendChild(li);
                    } 
                    if (data.endereco) {
                        const li = document.createElement('li');
                        li.textContent = data.errors;
                        errorList.appendChild(li);
                    }
                }
            })
            .catch(error => {
                console.error("Ocorreu um erro:", error);
                alert("Ocorreu um erro: " + error.message);
            });
        } catch (error) {
            console.error('Erro ao converter para JSON:', error);
        }
    });
    excluirBtn.addEventListener('click', function (event){
        const id_empresa = form_exclusao.elements['id_exclusao_empresa'].value;
        const url = `/empresa/${id_empresa}`
            // Fazendo a requisição AJAX
            fetch(url, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            }).then(response => {
                if (!response.ok) {
                    throw new Error("Erro na resposta da requisição");
                }
                return response.json();
            }).then(data => {
                if (data.success) {
                    location.reload(true)
            }}).catch(error => {
                console.error("Ocorreu um erro:", error);
                alert("Ocorreu um erro: " + error.message);
            });
            
    });

});

$(document).ready(function(){
    $('.telefone_empresa').mask('(00)00000-0000');
});