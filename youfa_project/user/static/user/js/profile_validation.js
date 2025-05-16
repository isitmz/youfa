$(document).ready(function () {
    console.log("Jquery caricato - edit_profile.js");

    // Limite data nascita - almeno 18 anni (utile se abilitassi il campo)
    let today = new Date();
    let minAge = 18;
    let maxDate = new Date(today.getFullYear() - minAge, today.getMonth(), today.getDate());
    let maxDateStr = maxDate.toISOString().split('T')[0];
    $('#id_data_nascita').attr('max', maxDateStr);

    function setInvalid(selector, message) {
        const field = $(selector);
        field.addClass('is-invalid');
        // Se non esiste già il feedback, lo aggiungiamo
        if (field.next('.invalid-feedback').length === 0) {
            field.after(`<div class="invalid-feedback">${message}</div>`);
        }
    }

    function clearInvalid(selector) {
        const field = $(selector);
        field.removeClass('is-invalid');
        field.next('.invalid-feedback').remove();
    }

    // Al cambio input puliamo errori
    $('#editProfileForm input').on('input', function () {
        clearInvalid(this);
    });

    $('#editProfileForm').on('submit', function (e) {
        // Pulisce errori precedenti
        $('.is-invalid').removeClass('is-invalid');
        $('.invalid-feedback').remove();

        let telefono = $('#id_telefono').val().trim();
        let isValid = true;

        // Validazione telefono: solo cifre, 7-15 caratteri
        if (!/^\d{7,15}$/.test(telefono)) {
            setInvalid('#id_telefono', "Inserisci un numero valido di 7-15 cifre.");
            isValid = false;
        }

        if (!isValid) {
            e.preventDefault();
        }
    });
});
