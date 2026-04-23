function rowTemplate(name = "", url = "") {
  const row = document.createElement("tr");
  row.innerHTML = `
    <td><input type="text" class="hotel-name" value="${name}" /></td>
    <td><input type="url" class="hotel-url" value="${url}" /></td>
    <td><button class="danger delete-hotel">Usuń</button></td>
  `;
  row.querySelector(".delete-hotel").addEventListener("click", () => row.remove());
  return row;
}

function bindDeleteHandlers() {
  document.querySelectorAll(".delete-hotel").forEach((btn) => {
    btn.onclick = () => btn.closest("tr").remove();
  });
}

function collectConfig() {
  const hotels = [...document.querySelectorAll("#hotels-table-body tr")]
    .map((row) => ({
      name: row.querySelector(".hotel-name")?.value?.trim(),
      url: row.querySelector(".hotel-url")?.value?.trim(),
    }))
    .filter((hotel) => hotel.name && hotel.url);

  return {
    hotels,
    dates: {
      check_in: document.getElementById("check-in").value,
      check_out: document.getElementById("check-out").value,
    },
  };
}

async function postJson(url, payload) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`Błąd HTTP: ${response.status}`);
  }
  return response.json();
}

function setStatus(message) {
  document.getElementById("status-box").textContent =
    typeof message === "string" ? message : JSON.stringify(message, null, 2);
}

document.getElementById("add-hotel").addEventListener("click", () => {
  document.getElementById("hotels-table-body").appendChild(rowTemplate());
});

document.getElementById("save-config").addEventListener("click", async () => {
  try {
    setStatus("Zapisywanie ustawień...");
    const result = await postJson("/api/config", collectConfig());
    setStatus({ message: "Ustawienia zapisane", result });
  } catch (error) {
    setStatus(`Nie udało się zapisać ustawień: ${error.message}`);
  }
});

document.getElementById("run-analysis").addEventListener("click", async () => {
  try {
    setStatus("Uruchamianie analizy...");
    const result = await postJson("/api/analyze", collectConfig());
    setStatus({ message: "Analiza zakończona", result });
  } catch (error) {
    setStatus(`Nie udało się uruchomić analizy: ${error.message}`);
  }
});

bindDeleteHandlers();
