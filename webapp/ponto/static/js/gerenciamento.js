document.addEventListener('DOMContentLoaded', function () {
    
    const excluirBtns = document.querySelectorAll('.btn-excluir');
    const editarBtns = document.querySelectorAll('.btn-editar');


    editarBtns.forEach(function (btn) {
        btn.addEventListener('click', function () {
            const id = btn.getAttribute('data-id');
            const nome = btn.getAttribute('data-nome');
            const endereco = btn.getAttribute('data-endereco');
            const telefone = btn.getAttribute('data-telefone');

            // Preenche os campos do formulário com os valores da empresa
            document.getElementById('id_empresa').value = id;
            document.getElementById('nome').value = nome;
            document.getElementById('endereco').value = endereco;
            document.getElementById('telefone').value = telefone;
        });
    });
    excluirBtns.forEach(function (btn) {
        btn.addEventListener('click', function () {
            const id = btn.getAttribute('data-id');
            const form_exclusao = document.getElementById('form_exclusao_empresa');
            form_exclusao.elements['id_exclusao_empresa'].value = id;
        });
    });

});