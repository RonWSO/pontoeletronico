document.addEventListener('DOMContentLoaded', function () {
    const adicionarBtn = document.getElementById('adicionarPonto');
    const editarFuncionarioBtn = document.getElementById('editarFuncionario');
    const form_ponto = document.getElementById('form_adicao_ponto');
    const form = document.getElementById('formulario_funcionario');
    
    adicionarBtn.addEventListener('click', function () {
        const id = adicionarBtn.getAttribute('data-id');
//        const form = document.getElementById('form_adicao_ponto');
        form_ponto.elements['id_funcionario'].value = id;
    });

    editarFuncionarioBtn.addEventListener('click', function () {
        const id = editarFuncionarioBtn.getAttribute('data-id');
        const id_empresa = editarFuncionarioBtn.getAttribute('data-empresa-id');
        console.log(id_empresa)
        const nome = editarFuncionarioBtn.getAttribute('data-nome');
        const email = editarFuncionarioBtn.getAttribute('data-email');
        const inicio_expediente = editarFuncionarioBtn.getAttribute('data-inicio-expediente');
        const horas_expediente = editarFuncionarioBtn.getAttribute('data-horario-expediente');
        const tempo_intervalo = editarFuncionarioBtn.getAttribute('data-tempo-intervalo');
//            const form_funcionario = document.getElementById('formulario_funcionario');
        // Preenche os campos do formulário com os valores da empresa
        form.elements['id_funcionario'].value = id;
        form.elements['id_empresa'].value = id_empresa;
        form.elements['nome_funcionario'].value = nome;
        form.elements['email_funcionario'].value = email;
        form.elements['inicio_expediente'].value = inicio_expediente;
        form.elements['horas_expediente'].value = horas_expediente;
        form.elements['tempo_intervalo'].value = tempo_intervalo;
        });

    const pontoBtn = document.getElementById('btn_marcar_ponto');
    const salvarBtn = document.getElementById('btn_salvar_funcionario');


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
        }).then(response =>response.json())
            .then(data => {
            if (data.success) {
                successAlert.style.display = 'block';
                errorAlert.style.display = 'none';
                form_ponto.reset()
            }else{
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

        const method = 'PUT';
        const url = `/funcionario/${id_funcionario}`

        if (!validEmail(email)){
            errorAlert.style.display = 'block';
            const li = document.createElement('li');
            li.textContent = "Formato do email inválido"
            errorList.appendChild(li);
            return
        }
        // Dados a serem enviados
        const data = {
            id_funcionario,
            nome,
            email,
            empresa,
            expediente: {
                inicio_expediente,
                horas_expediente,
                tempo_intervalo
            }
        };
        
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
                editarFuncionarioBtn.setAttribute('data-nome', nome);
                editarFuncionarioBtn.setAttribute('data-email', email);
                editarFuncionarioBtn.setAttribute('data-inicio-expediente', inicio_expediente); 
                editarFuncionarioBtn.setAttribute('data-horario-expediente', horas_expediente);
                editarFuncionarioBtn.setAttribute('data-tempo-intervalo', tempo_intervalo);
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
})