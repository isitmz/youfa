$(document).ready(function () {
  console.log("📈 Portfolio.js avviato (jQuery)");

  let capitaleInvestito = 0;
  let assetsData = []; // Per grafico a torta: { ticker, quantity }

  // Conta quanti ticker elaborare per sapere quando siamo a fine aggiornamento
  const totalAssets = $(".current-price").length;
  let processedAssets = 0;

  $(".current-price").each(function () {
    const $priceElem = $(this);
    const ticker = $priceElem.data("ticker");
    const $totalElem = $(`.total-value[data-ticker="${ticker}"]`);
    const quantity = parseFloat($totalElem.data("quantity"));

    // Salvo i dati per il grafico
    assetsData.push({ ticker, quantity });

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
      complete: function () {
        processedAssets++;
        if (processedAssets === totalAssets) {
          // Tutti i prezzi caricati: ora crea il grafico a torta
          createPieChart(assetsData);
        }
      },
    });
  });

  function createPieChart(data) {
    // Filtra solo asset con quantità > 0
    const filtered = data.filter((item) => item.quantity > 0);
    if (filtered.length === 0) {
      // Se non ci sono asset, mostra messaggio nel canvas
      const ctx = $("#portfolioPieChart")[0].getContext("2d");
      ctx.font = "16px Arial";
      ctx.fillText("Nessun asset da mostrare", 10, 50);
      return;
    }

    const labels = filtered.map((item) => item.ticker);
    const quantities = filtered.map((item) => item.quantity);

    const colors = [
      "#4e73df",
      "#1cc88a",
      "#36b9cc",
      "#f6c23e",
      "#e74a3b",
      "#858796",
      "#5a5c69",
      "#fd7e14",
      "#20c997",
      "#6610f2",
    ];

    new Chart($("#portfolioPieChart"), {
      type: "pie",
      data: {
        labels: labels,
        datasets: [
          {
            data: quantities,
            backgroundColor: colors.slice(0, labels.length),
            borderColor: "#fff",
            borderWidth: 2,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: "bottom",
            labels: { boxWidth: 20, padding: 15 },
          },
          tooltip: {
            callbacks: {
              label: (context) => {
                const label = context.label || "";
                const value = context.parsed || 0;
                return `${label}: ${value.toLocaleString()}`;
              },
            },
          },
        },
      },
    });
  }

  loadPortfolioHistory();
});


function loadPortfolioHistory() {
  $.get("/portfolio/history/", function (response) {
    const history = response.history;
    if (!history || history.length === 0) return;

    const labels = history.map((entry) => entry.date);
    const values = history.map((entry) => entry.value);

    const start = values[0];
    const end = values[values.length - 1];

    let lineColor = "#6c757d"; // grigio neutro
    if (end > start) lineColor = "#198754"; // verde (bootstrap success)
    else if (end < start) lineColor = "#dc3545"; // rosso (bootstrap danger)

    const ctx = document.getElementById("portfolioHistoryChart").getContext("2d");
    new Chart(ctx, {
      type: "line",
      data: {
        labels: labels,
        datasets: [{
          label: "Valore portafoglio",
          data: values,
          borderColor: lineColor,
          backgroundColor: hexToRgba(lineColor, 0.15),
          fill: true,
          tension: 0.3,
          pointRadius: 3,
          pointHoverRadius: 5,
        }],
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (ctx) => `$ ${ctx.parsed.y.toFixed(2)}`
            }
          }
        },
        scales: {
          y: {
            beginAtZero: false,
            ticks: {
              callback: (value) => `$ ${value.toFixed(0)}`
            }
          },
          x: {
            ticks: {
              maxTicksLimit: 8,
              autoSkip: true,
            }
          }
        }
      }
    });
  });
}

// Support function: HEX to RGBA
function hexToRgba(hex, alpha = 1) {
  const bigint = parseInt(hex.slice(1), 16);
  const r = (bigint >> 16) & 255;
  const g = (bigint >> 8) & 255;
  const b = bigint & 255;
  return `rgba(${r},${g},${b},${alpha})`;
}