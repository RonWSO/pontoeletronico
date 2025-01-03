
document.addEventListener('DOMContentLoaded', function () {
    var btnEditPressed;
    // Adiciona evento de clique ao botão "Editar"
    const editarBtns = document.querySelectorAll('.btn-editar');
    const adicionarBtn = document.getElementById('adicionarFuncionario');
    const excluirBtns = document.querySelectorAll('.btn-excluir');
    const pontoBtns = document.querySelectorAll('.btn-ponto');
    const relatorioBtns = document.querySelectorAll('.btn-relatório');

    adicionarBtn.addEventListener('click', function () {
        const id = adicionarBtn.getAttribute('data-id');
        const form = document.getElementById('formulario_funcionario');
        form.elements['id_empresa'].value = id;
    });

    editarBtns.forEach(function (btn) {
        btn.addEventListener('click', function () {
            btnEditPressed = btn
            const id = btn.getAttribute('data-id');
            const id_empresa = btn.getAttribute('data-empresa-id');
            const nome = btn.getAttribute('data-nome');
            const email = btn.getAttribute('data-email');
            const inicio_expediente = btn.getAttribute('data-inicio-expediente');
            const horas_expediente = btn.getAttribute('data-horario-expediente');
            const tempo_intervalo = btn.getAttribute('data-tempo-intervalo');
            // Preenche os campos do formulário com os valores da empresa
            document.getElementById('id_funcionario').value = id;
            document.getElementById('id_empresa').value = id_empresa;
            document.getElementById('nome_funcionario').value = nome;
            document.getElementById('email_funcionario').value = email;
            document.getElementById('inicio_expediente').value = inicio_expediente;
            document.getElementById('horas_expediente').value = horas_expediente;
            document.getElementById('tempo_intervalo').value = tempo_intervalo;
        });
    });

    excluirBtns.forEach(function (btn) {
        btn.addEventListener('click', function () {
            const id = btn.getAttribute('data-id');
            const form_exclusao = document.getElementById('form_exclusao_funcionario');
            form_exclusao.elements['id_exclusao_funcionario'].value = id;
        });
    });

    pontoBtns.forEach(function (btn) {
        btn.addEventListener('click', function () {
            const id = btn.getAttribute('data-id');
            const form_ponto = document.getElementById('form_adicao_ponto');
            form_ponto.elements['id_funcionario'].value = id;
        });
    });

    relatorioBtns.forEach(function (btn) {
        btn.addEventListener('click', function () {
            const id = btn.getAttribute('data-id');
            gerarRelatorio(id)
        });
    });

    const form = document.getElementById('formulario_funcionario');
    const form_exclusao = document.getElementById('form_exclusao_funcionario');
    const form_ponto = document.getElementById('form_adicao_ponto');
    const salvarBtn = document.getElementById('btn_salvar_funcionario');
    const excluirBtn = document.getElementById('btn_excluir_funcionario');
    const pontoBtn = document.getElementById('btn_marcar_ponto');

    pontoBtn.addEventListener('click', function (event) {
        event.preventDefault();
        const successAlert = document.querySelector('#alert-success-ponto');
        const errorAlert = document.querySelector('#alert-error-ponto');
        const errorList = errorAlert.querySelector('ul');

        const funcionario_id = form_ponto.elements['id_funcionario'].value;
        const data = form_ponto.elements['data_ponto'].value;
        const entrada_expediente = form_ponto.elements['entrada_expediente'].value;
        const saida_expediente = form_ponto.elements['saida_expediente'].value;
        const inicio_intervalo = form_ponto.elements['inicio_intervalo'].value;
        const saida_intervalo = form_ponto.elements['saida_intervalo'].value;
        const url = `/funcionario/${funcionario_id}/ponto`

        const dados = {
            funcionario_id,
            data,
            entrada_expediente,
            saida_expediente,
            inicio_intervalo,
            saida_intervalo,
        };
        // Converte os dados para JSON
        const body = JSON.stringify(dados);
        console.log(body)
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: body
        }).then(response =>response.json()).then(data => {
            if (data.success) {
                console.log(data);
                successAlert.style.display = 'block';
                errorAlert.style.display = 'none';
                form_ponto.reset()
            }else {
                console.log(data);
                errorAlert.style.display = 'block';
                errorList.innerHTML = ''; // Limpa a lista de erros
                // Tratando possíveis erros do backend
                if (data.saida_expediente) {
                    const li = document.createElement('li');
                    li.textContent = data.saida_expediente[0];
                    errorList.appendChild(li);
                } 
                if (data.saida_intervalo) {
                    const li = document.createElement('li');
                    li.textContent = data.saida_intervalo[0];
                    errorList.appendChild(li);
                }
                if (data.data) {
                    const li = document.createElement('li');
                    li.textContent = data.data[0];
                    errorList.appendChild(li);
                }
            }
        }).catch(error => {
            console.error("Ocorreu um erro:", error);
            alert("Ocorreu um erro: " + error.message);
        });
    });

    salvarBtn.addEventListener('click', function (event) {
        event.preventDefault();
        const successAlert = document.querySelector('#alert-success-funcionario');
        const errorAlert = document.querySelector('#alert-error-funcionario');
        const errorList = errorAlert.querySelector('ul');

        // Pegando os valores do formulário
        const nome = form.elements['nome_funcionario'].value;
        const email = form.elements['email_funcionario'].value;
        const inicio_expediente = form.elements['inicio_expediente'].value;
        const horas_expediente = form.elements['horas_expediente'].value;
        const tempo_intervalo = form.elements['tempo_intervalo'].value;
        const id_funcionario = form.elements['id_funcionario'].value;
        const empresa = form.elements['id_empresa'].value;

        const method = id_funcionario ? 'PUT' : 'POST';
        const url = id_funcionario ? `/funcionario/${id_funcionario}` : '/funcionario/';

        if (!validEmail(email)){
            errorAlert.style.display = 'block';
            const li = document.createElement('li');
            li.textContent = "Formato do email inválido"
            errorList.appendChild(li);
            return
        }
        // Dados a serem enviados
        const data = {
            nome,
            email,
            empresa,
            expediente: {
                inicio_expediente,
                horas_expediente,
                tempo_intervalo
            }
        };
        
        if (method === 'PUT') {
            data.id = id_funcionario;
        }
        
        // Converte os dados para JSON
        const body = JSON.stringify(data);
        fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: body
        })
        .then(response =>response.json())
        .then(data => {
            if (data.success) {
                successAlert.style.display = 'block';
                errorAlert.style.display = 'none';
                if(method === 'PUT'){
                    btnEditPressed.setAttribute('data-nome', nome);
                    btnEditPressed.setAttribute('data-email', email);
                    btnEditPressed.setAttribute('data-inicio-expediente', inicio_expediente); 
                    btnEditPressed.setAttribute('data-horario-expediente', horas_expediente);
                    btnEditPressed.setAttribute('data-tempo-intervalo', tempo_intervalo);
                }
                form.reset()
            } else {
                errorAlert.style.display = 'block';
                errorList.innerHTML = ''; // Limpa a lista de erros
                // Tratando possíveis erros do backend
                if (data.errors.email) {
                    const li = document.createElement('li');
                    li.textContent = data.errors.email;
                    errorList.appendChild(li);
                } 
                if (data.errors.nome) {
                    const li = document.createElement('li');
                    li.textContent = data.errors.nome;
                    errorList.appendChild(li);
                }
                if (data.errors.empresa) {
                    const li = document.createElement('li');
                    li.textContent = data.errors.empresa;
                    errorList.appendChild(li);
                }
                if (data.expediente) {
                    if (data.expediente.inicio_expediente) {
                        const li = document.createElement('li');
                        li.textContent = data.inicio_expediente;
                        errorList.appendChild(li);
                    }
                    if (data.expediente.horas_expediente) {
                        const li = document.createElement('li');
                        li.textContent = data.horas_expediente;
                        errorList.appendChild(li);
                    }
                    if (data.expediente.tempo_intervalo) {
                        const li = document.createElement('li');
                        li.textContent = data.tempo_intervalo;
                        errorList.appendChild(li);
                    }
                }
            }
        })
        .catch(error => {
            console.error("Ocorreu um erro:", error);
            alert("Ocorreu um erro: " + error.message);
        });
    });

    excluirBtn.addEventListener('click', function (event){
        const successAlert = document.querySelector('#alert-success-exclusao');
        const errorAlert = document.querySelector('#alert-error-exclusao');
        const errorList = errorAlert.querySelector('ul');

        const id_funcionario = form_exclusao.elements['id_exclusao_funcionario'].value;
        const url = `/funcionario/${id_funcionario}`
            // Fazendo a requisição AJAX
            fetch(url, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            }).then(response =>response.json())
            .then(data => {
                if (data.success) {
                    location.reload(true)
            }}).catch(error => {
                console.error("Ocorreu um erro:", error);
                alert("Ocorreu um erro: " + error.message);
            });
            
    });
})

function gerarRelatorio(id_funcionario){
    const url = `/funcionario/${id_funcionario}/relatorio`
    console.log(url)
    fetch(url, {
        method: 'GET',
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'relatorio.pdf';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    })
    .catch(error => {
        alert('Erro ao produzir o relatório.')
        console.error('Error:', error);
    });
}
