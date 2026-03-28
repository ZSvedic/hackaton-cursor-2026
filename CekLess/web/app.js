// #AI
const app = {
  procedures: [],
  regions: [],
  slots: [],

  async init() {
    const [procs, regs] = await Promise.all([
      fetch("/api/procedures").then(r => r.json()),
      fetch("/api/regions").then(r => r.json()),
    ]);
    this.procedures = procs;
    this.regions = regs;
    this.populateDatalist("proc-list", procs);
    this.populateDatalist("reg-list", regs);
    this.bindInputs();
  },

  populateDatalist(id, items) {
    const dl = document.getElementById(id);
    dl.innerHTML = items.map(i => `<option value="${i.Id} - ${i.Naziv}">`).join("");
  },

  bindInputs() {
    for (const prefix of ["proc", "reg"]) {
      const search = document.getElementById(`${prefix}-search`);
      const hidden = document.getElementById(prefix);
      const items = prefix === "proc" ? this.procedures : this.regions;
      search.addEventListener("change", () => {
        const match = items.find(i => `${i.Id} - ${i.Naziv}` === search.value);
        hidden.value = match ? match.Id : "";
      });
    }
  },

  async search(evt) {
    evt.preventDefault();
    const pid = document.getElementById("proc").value;
    const rid = document.getElementById("reg").value;
    if (!pid || !rid) {
      this.showStatus("Select both procedure and region.");
      return false;
    }
    this.showStatus("Searching...");
    this.closeCard();
    try {
      const res = await fetch(`/api/search?pid=${pid}&rid=${rid}`);
      const data = await res.json();
      if (data.error) { this.showStatus(`Error: ${data.error}`); return false; }
      if (!data.length) { this.showStatus("No results found."); return false; }
      this.slots = data;
      this.renderTable(data);
      this.showStatus(`Found ${data.length} slot(s).`);
    } catch (err) {
      this.showStatus(`Error: ${err.message}`);
    }
    return false;
  },

  renderTable(slots) {
    const cols = ["SlotID", "datetime", "waitDays", "hospital"];
    let html = '<table><thead><tr>';
    html += cols.map(c => `<th>${c}</th>`).join("");
    html += "</tr></thead><tbody>";
    for (const s of slots) {
      html += `<tr data-slot="${s.SlotID}" onclick="app.showCard(${s.SlotID})">`;
      html += cols.map(c => `<td>${s[c]}</td>`).join("");
      html += "</tr>";
    }
    html += "</tbody></table>";
    const el = document.getElementById("results");
    el.innerHTML = html;
    el.classList.remove("hidden");
  },

  async showCard(slotId) {
    const slot = this.slots.find(s => s.SlotID === slotId);
    if (!slot) return;

    document.querySelectorAll("#results tr.selected").forEach(r => r.classList.remove("selected"));
    const row = document.querySelector(`#results tr[data-slot="${slotId}"]`);
    if (row) row.classList.add("selected");

    let hospital = {};
    try {
      hospital = await fetch(`/api/hospital?email=${encodeURIComponent(slot.email)}`).then(r => r.json());
    } catch (_) { /* ignore */ }

    const emails = slot.email.split(",").map(e => e.trim());
    const webUrl = (hospital.webUrl || "").trim();
    const domain = emails[0].split("@")[1] || "";
    const web = webUrl || (domain ? `https://${domain}` : "");

    let html = `<div class="card-header">
      <h3>Slot ${slot.SlotID} — ${slot.datetime}</h3>
      <p>${slot.hospital} &middot; ${slot.waitDays} days wait</p>
    </div><div class="card-inner"><div class="card-grid">`;

    html += `<div class="card-label">Email</div><div class="card-value">`;
    for (const email of emails) {
      html += `<a href="mailto:${email}?subject=Appointment&body=Hello">${email}</a>`;
    }
    html += `</div>`;

    html += `<div class="card-label">Phone</div><div class="card-value">`;
    html += `<a href="tel:${slot.telefon}">${slot.telefon}</a>`;
    if (slot.telefaks) html += `<br>Fax: ${slot.telefaks}`;
    html += `</div>`;

    if (web) {
      html += `<div class="card-label">Website</div><div class="card-value"><a href="${web}" target="_blank">${web}</a></div>`;
    }
    if (hospital.address) {
      html += `<div class="card-label">Address</div><div class="card-value">${hospital.address}</div>`;
    }
    if (hospital.bookingUrl) {
      html += `<div class="card-label">Booking</div><div class="card-value"><a href="${hospital.bookingUrl}" target="_blank">Book online</a></div>`;
    }
    if (hospital.mapsUrl) {
      html += `<div class="card-label">Map</div><div class="card-value"><a href="${hospital.mapsUrl}" target="_blank">View on Google Maps</a></div>`;
    }

    html += "</div></div>";

    document.getElementById("card-content").innerHTML = html;
    document.getElementById("card-panel").classList.add("open");
  },

  closeCard() {
    document.getElementById("card-panel").classList.remove("open");
    document.querySelectorAll("#results tr.selected").forEach(r => r.classList.remove("selected"));
  },

  showStatus(msg) {
    const el = document.getElementById("status");
    el.textContent = msg;
    el.classList.remove("hidden");
  },

  hide(id) {
    document.getElementById(id).classList.add("hidden");
  },
};

app.init();
