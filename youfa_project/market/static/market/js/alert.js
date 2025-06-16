$(document).ready(function () {
  // Crea un nuovo alert
  $("#create-alert-btn").on("click", function () {
    const ticker = $(this).data("ticker");
    const targetPrice = parseFloat($("#alert-price").val());
    const direction = $("#alert-direction").val();
    const $messageBox = $("#alert-message");

    $messageBox.html("");

    if (!ticker || isNaN(targetPrice) || targetPrice <= 0) {
      $messageBox.html(
        '<div class="alert alert-danger">Inserisci un prezzo valido maggiore di 0.</div>'
      );
      return;
    }

    const csrfToken = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
      url: "api/create-price-alert/",
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
      },
      data: {
        ticker: ticker,
        target_price: targetPrice,
        direction: direction,
      },
      success: function (data) {
        const alertClass = data.success ? "alert-success" : "alert-danger";
        $messageBox.html(`<div class="alert ${alertClass}">${data.message}</div>`);

        if (data.success) {
          $("#alert-price").val("");
          loadUserAlerts(ticker); // aggiorna lista alert
        }
      },
      error: function () {
        $messageBox.html(
          '<div class="alert alert-danger">Errore durante la creazione dell\'alert.</div>'
        );
      },
    });
  });

  // Cancella un alert
  $(document).on("click", ".delete-alert-btn", function () {
    const alertId = $(this).data("alert-id");
    const ticker = $(this).data("ticker");
    const csrfToken = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
      url: "api/delete-price-alert/",
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
      },
      data: {
        alert_id: alertId,
      },
      success: function (data) {
        if (data.success) {
          // Rimuovi direttamente dalla lista
          $(`#alert-item-${alertId}`).remove();

          // Se la lista è vuota, mostra un messaggio
          if ($("#existing-alerts .alert").length === 0) {
            $("#existing-alerts").html('<p class="text-muted">Nessun alert attivo.</p>');
          }
        }
      },
      error: function () {
        console.error("Errore durante l'eliminazione dell'alert.");
      },
    });
  });

  // Carica alert esistenti
  function loadUserAlerts(ticker) {
    $.ajax({
      url: `api/get-user-alerts/${ticker}/`,
      method: "GET",
      success: function (data) {
        const $container = $("#existing-alerts");
        $container.empty();

        if (data.alerts.length === 0) {
          $container.html('<p class="text-muted">Nessun alert attivo.</p>');
        } else {
          data.alerts.forEach((alert) => {
            const icon = alert.direction === 'above' ? '⬆️' : '⬇️';
            const alertHtml = `
              <div id="alert-item-${alert.id}" class="alert alert-light d-flex justify-content-between align-items-center">
                <span>${icon} ${alert.target_price} $</span>
                <button class="btn btn-sm btn-outline-danger delete-alert-btn" data-alert-id="${alert.id}" data-ticker="${ticker}" title="Elimina alert">
                  <i class="bi bi-x-lg"></i>
                </button>
              </div>
            `;
            $container.append(alertHtml);
          });
        }
      },
      error: function () {
        console.error("Errore nel caricamento degli alert.");
      },
    });
  }

  // Rende la funzione disponibile globalmente
  window.loadUserAlerts = loadUserAlerts;
});