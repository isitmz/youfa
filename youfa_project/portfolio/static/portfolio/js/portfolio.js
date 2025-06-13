$(document).ready(function () {
  console.log("📈 Portfolio.js avviato (jQuery)");

  let capitaleInvestito = 0;

  $(".current-price").each(function () {
    const $priceElem = $(this);
    const ticker = $priceElem.data("ticker");
    const $totalElem = $(`.total-value[data-ticker="${ticker}"]`);
    const quantity = parseFloat($totalElem.data("quantity"));

    $.ajax({
      url: `/market/api/price/${ticker}/`,
      method: "GET",
      success: function (data) {
        if (data.price) {
          const price = parseFloat(data.price);
          $priceElem.text(`$ ${price.toFixed(2)}`);

          const total = quantity * price;
          $totalElem.text(`$ ${total.toFixed(2)}`);

          capitaleInvestito += total;
          $("#invested-capital").text(`$ ${capitaleInvestito.toFixed(2)}`);
        } else {
          $priceElem.text("N/D");
          $totalElem.text("N/D");
        }
      },
      error: function () {
        console.error(`❌ Errore prezzo per ${ticker}`);
        $priceElem.text("Errore");
        $totalElem.text("Errore");
      },
    });

  });
});
