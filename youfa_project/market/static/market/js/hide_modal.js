$(document).ready(function () {
  // Quando il modal viene chiuso (evento Bootstrap)
  $("#detailsModal").on("hidden.bs.modal", function () {
    console.log("🔄 Pulizia modal alla chiusura");

    // Svuota testi e messaggi
    $("#modal-name").text("");
    $("#modal-price").text("");
    $("#modal-quantity").text("—");
    $("#modal-average-price").text("—");
    $("#trade-message").text("").removeClass("text-danger text-success");

    // Svuota input quantità trade
    $("#trade-quantity").val("");

    // Svuota informazioni aggiuntive
    $("#additional-info").empty();

    // Nascondi grafico e distruggi istanza se presente
    $("#priceChart").hide();
    /*
    if (chartInstance || chartInstance != null) {
      chartInstance.destroy();
      chartInstance = null;
    }*/

    // Reset ticker corrente
    currentTicker = null;
  });
});
