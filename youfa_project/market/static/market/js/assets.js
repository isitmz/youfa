$(document).ready(function() {
    console.log("🟢 DOM pronto. Avvio caricamento prezzi.");

    // Carica i prezzi semplici per ogni asset nella lista
    $(".price").each(function() {
        const ticker = $(this).data("ticker");
        const $priceElem = $(this);

        console.log(`🔄 Caricamento prezzo per ${ticker}...`);

        $.ajax({
            url: `api/price/${ticker}/`,
            method: "GET",
            success: function(data) {
                console.log(`✅ Prezzo ricevuto per ${ticker}:`, data);
                if (data.price) {
                    $priceElem.text(`Prezzo: ${data.price} ${data.currency}`);
                }
            },
            error: function() {
                console.error(`❌ Errore nel caricamento del prezzo per ${ticker}`);
                $priceElem.text("Prezzo: dati non disponibili");
            },
        });
    });

    // Istanza globale del modal Bootstrap
    const modalEl = document.getElementById("detailsModal");
    const modal = new bootstrap.Modal(modalEl);
    let chartInstance = null;
    let currentTicker = null;

    // Bottone dettagli: usa api/details per dati completi
    $(".details-btn").click(function() {
        const ticker = $(this).data("ticker");
        currentTicker = ticker;        
        console.log(`🔍 Richiesta dettagli per ${ticker}`);

        // Pulisci modal
        $("#modal-name").text("");
        $("#modal-price").text("");
        $("#additional-info").empty();

        // 🔄 Carica gli alert esistenti per il ticker selezionato
        loadUserAlerts(ticker);

        // Mostra il modal
        modal.show();

        $.ajax({
            url: `api/details/${ticker}/`,
            method: "GET",
            success: function(data) {
                console.log(`✅ Dettagli ricevuti per ${ticker}:`, data);

                if (data.error) {
                    console.warn(`⚠️ Errore nei dettagli per ${ticker}:`, data.error);
                    $("#modal-name").text("Errore");
                    $("#modal-price").text("");
                    $("#additional-info").html(`<p class="text-danger">${data.error}</p>`);
                    if (chartInstance) {
                        chartInstance.destroy();
                        chartInstance = null;
                    }
                    $("#priceChart").hide();
                    return;
                }

                // Imposta nome e prezzo in alto
                $("#modal-name").text(`${data.name} (${data.ticker})`);
                $("#modal-price").text(`${data.price} ${data.currency}`);

                // Impostiamo il bottone dell'alert
                $("#create-alert-btn").data("ticker", ticker);

                // Info aggiuntive in due colonne
                const leftCol = `
                    <p><strong>Settore:</strong> ${data.sector || "-"}</p>
                    <p><strong>Industria:</strong> ${data.industry || "-"}</p>
                    <p><strong>Capitalizzazione:</strong> ${data.market_cap ? data.market_cap.toLocaleString() : "-"}</p>
                    <p><strong>P/E ratio:</strong> ${data.pe_ratio || "-"}</p>
                `;
                const rightCol = `
                    <p><strong>Dividend Yield:</strong> ${data.dividend_yield || "-"}</p>
                    <p><strong>Volume medio:</strong> ${data.average_volume ? data.average_volume.toLocaleString() : "-"}</p>
                    <p><strong>Variazione % (oggi):</strong> ${data.change_percent || "-"}%</p>
                `;

                $("#additional-info").html(`
                    <div class="col-md-6">${leftCol}</div>
                    <div class="col-md-6">${rightCol}</div>
                    <div class="col-12 mt-3">
                        <p><strong>Descrizione:</strong> ${data.description || "N/A"}</p>
                    </div>
                `);

                // Carica il grafico con i dati storici
                loadChart(ticker);
            },
            error: function() {
                console.error(`❌ Errore nel caricamento dei dettagli per ${ticker}`);
                $("#modal-name").text("Errore nel caricamento dei dettagli");
                $("#modal-price").text("");
                $("#additional-info").html('<p class="text-danger">Errore nel caricamento dei dettagli</p>');
                if (chartInstance) {
                    chartInstance.destroy();
                    chartInstance = null;
                }
                $("#priceChart").hide();
            },
        });
    });

    // Ridisegna il grafico quando il modal viene mostrato
    modalEl.addEventListener('shown.bs.modal', function () {
        if (currentTicker && chartInstance) {
            console.log(`🔄 Ridisegno grafico per ${currentTicker} dopo apertura modal`);
            chartInstance.resize();
            chartInstance.update();
        }
    });

    function loadChart(ticker) {
        console.log(`📈 Caricamento dati grafico per ${ticker}`);
        $.ajax({
            url: `api/chart/${ticker}/`,
            method: "GET",
            success: function(data) {
                console.log(`✅ Dati grafico ricevuti per ${ticker}:`, data);

                if (!data || !data.data || data.data.length === 0) {
                    console.warn(`⚠️ Nessun dato storico disponibile per ${ticker}`);
                    $("#priceChart").hide();
                    if (chartInstance) {
                        chartInstance.destroy();
                        chartInstance = null;
                    }
                    return;
                }

                $("#priceChart").show();

                const labels = data.data.map(point => point.date);
                const prices = data.data.map(point => point.close);

                const ctx = document.getElementById("priceChart").getContext("2d");

                if (chartInstance) {
                    chartInstance.destroy();
                }

                chartInstance = new Chart(ctx, {
                    type: "line",
                    data: {
                        labels: labels,
                        datasets: [{
                            label: `${ticker} - Prezzo di chiusura`,
                            data: prices,
                            borderColor: "rgba(75, 192, 192, 1)",
                            backgroundColor: "rgba(75, 192, 192, 0.15)",
                            fill: true,
                            tension: 0.3,
                            pointRadius: 3,
                            pointHoverRadius: 6,
                            borderWidth: 2,
                        }],
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        interaction: {
                            mode: "index",
                            intersect: false,
                        },
                        plugins: {
                            tooltip: {
                                enabled: true,
                                callbacks: {
                                    label: function(context) {
                                        const price = context.parsed.y;
                                        return ` Prezzo: ${price}`;
                                    },
                                },
                            },
                            legend: {
                                display: true,
                                position: "top",
                            },
                        },
                        scales: {
                            x: {
                                display: true,
                                title: {
                                    display: true,
                                    text: "Data",
                                    color: "#888",
                                },
                                ticks: {
                                    autoSkip: true,
                                    maxTicksLimit: 10,
                                    callback: function(value) {
                                        const label = this.getLabelForValue(value);
                                        const date = new Date(label);
                                        return date.toLocaleDateString("it-IT", {
                                            month: "short",
                                            day: "numeric",
                                        });
                                    },
                                },
                            },
                            y: {
                                display: true,
                                title: {
                                    display: true,
                                    text: "Prezzo",
                                    color: "#888",
                                },
                                beginAtZero: false,
                            },
                        },
                        animation: {
                            duration: 800,
                            easing: "easeOutQuart",
                        },
                    },
                });
            },
            error: function() {
                console.error(`❌ Errore nel caricamento del grafico per ${ticker}`);
                $("#priceChart").hide();
                if (chartInstance) {
                    chartInstance.destroy();
                    chartInstance = null;
                }
            },
        });
    }
});