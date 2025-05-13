$(document).ready(function () {
    console.log("Jquery caricato");

    let today = new Date();
    let minAge = 18;
    let maxDate = new Date(today.getFullYear() - minAge, today.getMonth(), today.getDate());
    let maxDateStr = maxDate.toISOString().split('T')[0];
    $('#data_nascita').attr('max', maxDateStr);

    function setInvalid(selector, message) {
        const field = $(selector);
        field.addClass('is-invalid');
        if (!field.next('.invalid-feedback').length) {
            field.after(`<div class="invalid-feedback">${message}</div>`);
        }
    }

    function clearInvalid(selector) {
        const field = $(selector);
        field.removeClass('is-invalid');
        field.next('.invalid-feedback').remove();
    }

    $('#registrationForm input').on('input', function () {
        clearInvalid(this);
    });

    $('#registrationForm').on('submit', function (e) {
        $('.is-invalid').removeClass('is-invalid');
        $('.invalid-feedback').remove();

        let cf = $('#codice_fiscale').val().trim();
        let tel = $('#telefono').val().trim();
        let pwd = $('#password').val();
        let confirmPwd = $('#confirm_password').val();

        let isValid = true;

        // Codice Fiscale base
        if (!/^[A-Z]{6}[0-9]{2}[A-Z][0-9]{2}[A-Z][0-9]{3}[A-Z]$/i.test(cf)) {
            setInvalid('#codice_fiscale', "Formato del codice fiscale non valido.");
            isValid = false;
        } else {
            let cf_upper = cf.toUpperCase();
            let year = parseInt(cf_upper.substring(6, 8));
            let monthCode = cf_upper.substring(8, 9);
            let day = parseInt(cf_upper.substring(9, 11));
            let monthMap = "ABCDEHLMPRST";
            let monthIndex = monthMap.indexOf(monthCode);

            if (isNaN(year) || year < 0 || year > 99) {
                setInvalid('#codice_fiscale', "Anno di nascita non valido nel codice fiscale.");
                isValid = false;
            } else if (monthIndex === -1) {
                setInvalid('#codice_fiscale', "Mese di nascita non valido nel codice fiscale.");
                isValid = false;
            } else {
                let isFemale = day > 40;
                let actualDay = isFemale ? day - 40 : day;

                if (actualDay < 1 || actualDay > 31) {
                    setInvalid('#codice_fiscale', "Giorno di nascita non valido nel codice fiscale.");
                    isValid = false;
                }

                if ((monthIndex == 1 && actualDay > 29) ||
                    ([3, 5, 8, 10].includes(monthIndex) && actualDay > 30)) {
                    setInvalid('#codice_fiscale', "Giorno non valido per il mese specificato nel codice fiscale.");
                    isValid = false;
                }
            }
        }

        // Telefono
        if (!/^\d{7,15}$/.test(tel)) {
            setInvalid('#telefono', "Inserisci un numero valido di 7-15 cifre.");
            isValid = false;
        }

        // Password
        if (pwd.length < 8) {
            setInvalid('#password', "La password deve contenere almeno 8 caratteri.");
            isValid = false;
        }

        if (pwd !== confirmPwd) {
            setInvalid('#confirm_password', "Le password non corrispondono.");
            isValid = false;
        }

        if (!isValid) e.preventDefault();
    });
});
