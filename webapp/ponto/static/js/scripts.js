function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function validEmail(email){
    return /^[\w+.]+@\w+\.\w{2,}(?:\.\w{2})?$/.test(email)
}
$(document).ready(function() {
    $('#pontoModal').on('hidden.bs.modal', function () {
        hide_alerts();
    })
    $('#ExcluirFuncionarioModal').on('hidden.bs.modal', function () {
        hide_alerts();
    })
    $('#FuncionarioModal').on('hidden.bs.modal', function () {
        hide_alerts();
    })
    function hide_alerts(){
        $('.alert-danger').hide(); 
        $('.alert-success').hide(); 
    }
})