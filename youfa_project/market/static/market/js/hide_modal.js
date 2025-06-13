$(document).ready(function () {
  $("#detailsModal").on("hidden.bs.modal", function () {
    console.log("🔄 Pulizia completa del modal");

    // Reset titoli e prezzo
    $("#modal-name").text("");
    $("#modal-price").text("");

    // Reset informazioni utente
    $("#modal-balance").text("$ -");
    $("#modal-quantity").text("0");
    $("#modal-average-price").text("0.00");

    // Reset campo input quantità
    $("#trade-quantity").val("");

    // Reset messaggi di stato
    $("#estimated-total").text("Totale stimato: -");
    $("#trade-message").text("").removeClass("text-success text-danger");

    // Svuota le info aggiuntive
    $("#additional-info").empty();

    // Nasconde e distrugge grafico se esiste
    if (window.priceChartInstance) {
      window.priceChartInstance.destroy();
      window.priceChartInstance = null;
    }
    $("#priceChart").hide();

    // Reset variabili globali di stato se presenti
    window.currentTicker = null;
  });
});
