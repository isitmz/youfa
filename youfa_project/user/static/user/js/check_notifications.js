$(document).ready(function () {
  function fetchNotifications() {
    console.log("Inizio fetch notifiche...");

    $.ajax({
      url: "/user/api/notifications",
      method: "GET",
      dataType: "json",
      success: function (data) {
        let notifications = data.notifications;
        let container = $("#notifications-container");
        console.log("Notifiche ricevute:", notifications.length);
        container.empty();

        // Header fisso
        container.append('<h5 class="mb-3">📢 Notifiche recenti</h5>');

        if (notifications.length === 0) {
          container.append('<p class="text-muted mb-0">Nessuna notifica per ora.</p>');
        } else {
          let ul = $('<ul class="list-unstyled mb-0"></ul>');
          notifications.forEach(function (notif) {
            // formattiamo la data come d/m/Y H:i (puoi modificare se il backend la manda già formattata)
            let dateFormatted = notif.created_at; // Se serve puoi usare moment.js o simili per formattare lato client

            let li = $(`
              <li class="mb-2">
                <span>${notif.message}</span><br/>
                <small class="text-muted">${dateFormatted}</small>
              </li>
            `);
            ul.append(li);
          });
          container.append(ul);
        }
      },
      error: function () {
        console.error("Errore nel recupero delle notifiche.");
        console.error("Errore nel recupero delle notifiche.");
      },
    });
  }

  console.log("check_notifications.js caricato e pronto.");
  fetchNotifications();

  // Per aggiornare ogni 30s (esempio), scommentare:
  // setInterval(fetchNotifications, 30000);
});