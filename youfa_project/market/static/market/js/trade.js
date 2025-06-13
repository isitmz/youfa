$(document).ready(function () {
  let currentTicker = null;

  // Click su bottone dettagli: aggiorna solo quantità e prezzo medio
  $(".details-btn").click(function () {
    const ticker = $(this).data("ticker");
    currentTicker = ticker;

    // Check con variabile assegnata da Django in base alla sessione dell'utente
    if (isLoggedIn) {
      console.log(`🟢 Trade.js: richiesta portfolio-info per ${ticker}`);

      // Questa richiesta serve per recuperare i dati di un'azione di un utente (se la possiede)
      $.ajax({
        url: `/portfolio/api/portfolio-info/${ticker}/`,
        method: "GET",
        success: function (data) {
          $("#modal-quantity").text(data.quantity.toFixed(2));
          $("#modal-average-price").text(data.avg_price.toFixed(2));
        },
        error: function () {
          $("#modal-quantity").text("0");
          $("#modal-average-price").text("0.00");
        },
      });

      // Recupero saldo
      $.ajax({
        url: "/portfolio/api/portfolio-balance/",
        method: "GET",
        success: function (data) {
          $("#modal-balance").text(`$ ${data.saldo.toFixed(2)}`);
        },
        error: function () {
          $("#modal-balance").text("$ -");
        },
      });
    }
  });

  // Submit del form per compra/vendi
  $("#trade-form").submit(function (e) {
    e.preventDefault();

    const quantity = parseInt($("#trade-quantity").val(), 10);
    if (!quantity || quantity < 1) {
      $("#trade-message")
        .text("Inserisci una quantità valida (>=1).")
        .removeClass("text-success")
        .addClass("text-danger");
      return;
    }

    const operation = $(document.activeElement).data("action");
    if (!operation || (operation !== "buy" && operation !== "sell")) {
      $("#trade-message")
        .text("Azione non riconosciuta.")
        .removeClass("text-success")
        .addClass("text-danger");
      return;
    }

    // Prendo il prezzo da #modal-price (es. "123.45 USD")
    const priceText = $("#modal-price")
      .text()
      .replace(/[^0-9.,]/g, "");
    const price = parseFloat(priceText.replace(",", "."));
    if (!price || price <= 0) {
      $("#trade-message")
        .text("Prezzo non valido.")
        .removeClass("text-success")
        .addClass("text-danger");
      return;
    }

    const data = {
      ticker: currentTicker,
      operation: operation,
      quantity: quantity,
      price: price,
    };

    // console.log("Request buy per " + data);

    $.ajax({
      url: "/market/api/trade/",
      method: "POST",
      contentType: "application/json",
      data: JSON.stringify(data),
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
      success: function (response) {
        $("#trade-message")
          .text(response.message)
          .removeClass("text-danger")
          .addClass("text-success");

        // Aggiorna saldo
        $("#user-balance").text(`$ ${response.saldo.toFixed(2)}`);

        $("#modal-balance").text(`$ ${response.saldo.toFixed(2)}`);

        // Aggiorna quantità e prezzo medio
        $("#modal-quantity").text(response.quantity.toFixed(2));
        $("#modal-average-price").text(response.avg_price.toFixed(2));
      },
      error: function (xhr) {
        const err = xhr.responseJSON?.error || "Errore nella transazione.";
        $("#trade-message")
          .text(err)
          .removeClass("text-success")
          .addClass("text-danger");
      },
    });
  });

  // CSRF token da cookie
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  // Aggiorna il totale stimato ogni volta che cambia la quantità
  $("#trade-quantity").on("change", function () {
    const quantity = parseInt($(this).val(), 10);

    // Ottieni il prezzo attuale dal DOM
    const priceText = $("#modal-price").text(); // es. "123.45 USD"
    const match = priceText.match(/([\d,.]+)/);

    if (!match) {
      $("#estimated-total").text("Totale stimato: -");
      return;
    }

    const price = parseFloat(match[1].replace(",", "."));

    if (isNaN(quantity) || quantity <= 0 || isNaN(price)) {
      $("#estimated-total").text("Totale stimato: -");
      return;
    }

    const total = (quantity * price).toFixed(2);
    $("#estimated-total").text(`Totale stimato: $ ${total}`);
  });
});
