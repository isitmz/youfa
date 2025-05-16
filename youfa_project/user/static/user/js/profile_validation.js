$(document).ready(function () {
    console.log("Jquery caricato - profile_validation.js");

    let today = new Date();
    let minAge = 18;
    let maxDate = new Date(today.getFullYear() - minAge, today.getMonth(), today.getDate());
    let maxDateStr = maxDate.toISOString().split('T')[0];
    $('#id_data_nascita').attr('max', maxDateStr);

    function setInvalid(selector, message) {
        const field = $(selector);
        field.addClass('is-invalid');
        if (field.next('.invalid-feedback').length === 0) {
            field.after(`<div class="invalid-feedback">${message}</div>`);
        }
    }

    function clearInvalid(selector) {
        const field = $(selector);
        field.removeClass('is-invalid');
        field.next('.invalid-feedback').remove();
    }

    // Pulizia errori su input
    $('form input').on('input', function () {
        clearInvalid(this);
    });

    // Aggiunge class="form-control" ai campi password se mancante
    $('#changePasswordForm input[type="password"]').each(function () {
        if (!$(this).hasClass('form-control')) {
            $(this).addClass('form-control');
        }
    });

    $('#editProfileForm').on('submit', function (e) {
        $('.is-invalid').removeClass('is-invalid');
        $('.invalid-feedback').remove();

        let telefono = $('#id_telefono').val().trim();
        let isValid = true;

        if (!/^\d{7,15}$/.test(telefono)) {
            setInvalid('#id_telefono', "Inserisci un numero valido di 7-15 cifre.");
            isValid = false;
        }

        if (!isValid) {
            e.preventDefault();
        }
    });

    $('#changePasswordForm').on('submit', function (e) {
        $('.is-invalid').removeClass('is-invalid');
        $('.invalid-feedback').remove();

        let currentPassword = $('#id_old_password').val().trim();
        let newPassword1 = $('#id_new_password1').val().trim();
        let newPassword2 = $('#id_new_password2').val().trim();
        let isValid = true;

        if (currentPassword === '') {
            setInvalid('#id_old_password', "Inserisci la password attuale.");
            isValid = false;
        }

        if (newPassword1 === '') {
            setInvalid('#id_new_password1', "Inserisci una nuova password.");
            isValid = false;
        } else if (newPassword1.length < 8) {
            setInvalid('#id_new_password1', "La nuova password deve contenere almeno 8 caratteri.");
            isValid = false;
        }

        if (newPassword2 === '') {
            setInvalid('#id_new_password2', "Conferma la nuova password.");
            isValid = false;
        } else if (newPassword1 !== newPassword2) {
            setInvalid('#id_new_password2', "Le due password non corrispondono.");
            isValid = false;
        }

        if (!isValid) {
            e.preventDefault();
        }
    });
});
