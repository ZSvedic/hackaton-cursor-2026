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
    this.hide("card");
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
    let html = '<table class="pure-table pure-table-striped"><thead><tr>';
    html += cols.map(c => `<th>${c}</th>`).join("");
    html += "</tr></thead><tbody>";
    for (const s of slots) {
      html += `<tr onclick="app.showCard(${s.SlotID})">`;
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
    let hospital = {};
    try {
      hospital = await fetch(`/api/hospital?email=${encodeURIComponent(slot.email)}`).then(r => r.json());
    } catch (_) { /* ignore */ }

    const emails = slot.email.split(",").map(e => e.trim());
    const webUrl = (hospital.webUrl || "").trim();
    const domain = emails[0].split("@")[1] || "";
    const web = webUrl || (domain ? `https://${domain}` : "");

    let html = `<div class="card"><h3>Slot ${slot.SlotID} — ${slot.datetime}</h3>`;
    html += `<p><strong>${slot.hospital}</strong><br>${slot.waitDays} days wait</p>`;
    html += `<div class="field-label">Email</div>`;
    for (const email of emails) {
      html += `<a href="mailto:${email}?subject=Appointment&body=Hello">${email}</a>`;
    }
    html += `<div class="field-label">Phone</div>`;
    html += `<a href="tel:${slot.telefon}">${slot.telefon}</a>`;
    if (slot.telefaks) html += `<span> Fax: ${slot.telefaks}</span>`;
    if (web) {
      html += `<div class="field-label">Website</div><a href="${web}" target="_blank">${web}</a>`;
    }
    if (hospital.address) {
      html += `<div class="field-label">Address</div><span>${hospital.address}</span>`;
    }
    if (hospital.bookingUrl) {
      html += `<div class="field-label">Online Booking</div><a href="${hospital.bookingUrl}" target="_blank">${hospital.bookingUrl}</a>`;
    }
    if (hospital.mapsUrl) {
      html += `<div class="field-label">Map</div><a href="${hospital.mapsUrl}" target="_blank">View on Google Maps</a>`;
    }
    html += "</div>";
    const el = document.getElementById("card");
    el.innerHTML = html;
    el.classList.remove("hidden");
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
