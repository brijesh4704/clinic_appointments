const API = "";
let token = localStorage.getItem("clinicflow_token") || "";

const $ = (id) => document.getElementById(id);

function apiHeaders() {
  const headers = { "Content-Type": "application/json" };
  if (token) headers.Authorization = `Bearer ${token}`;
  return headers;
}

function showToast(message) {
  const toast = $("toast");
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(window.toastTimer);
  window.toastTimer = setTimeout(() => toast.classList.remove("show"), 2600);
}

function openDashboard() {
  $("app").scrollIntoView({ behavior: "smooth", block: "start" });
  setTimeout(() => {
    if (token) showDashboard();
    else $("loginEmail").focus();
  }, 350);
}

document.querySelectorAll("[data-open-dashboard]").forEach(btn => {
  btn.addEventListener("click", openDashboard);
});

$("mobileMenu").addEventListener("click", () => $("mobileNav").classList.toggle("open"));
document.querySelectorAll("#mobileNav a").forEach(a => a.addEventListener("click", () => $("mobileNav").classList.remove("open")));

async function register() {
  const name = $("registerName").value.trim();
  const email = $("registerEmail").value.trim();
  const password = $("registerPassword").value;

  if (!name || !email || !password) {
    $("registerMessage").textContent = "Please fill all registration fields.";
    return;
  }

  try {
    const response = await fetch(`${API}/auth/register`, {
      method: "POST",
      headers: apiHeaders(),
      body: JSON.stringify({ name, email, password })
    });
    const data = await response.json();

    $("registerMessage").textContent = response.ok
      ? "Account created. You can now login."
      : (data.detail || "Registration failed.");

    if (response.ok) {
      $("loginEmail").value = email;
      $("loginPassword").value = password;
    }
  } catch {
    $("registerMessage").textContent = "Could not connect to the server.";
  }
}

async function login() {
  const email = $("loginEmail").value.trim();
  const password = $("loginPassword").value;

  if (!email || !password) {
    $("loginMessage").textContent = "Enter your email and password.";
    return;
  }

  try {
    const response = await fetch(`${API}/auth/login`, {
      method: "POST",
      headers: apiHeaders(),
      body: JSON.stringify({ email, password })
    });
    const data = await response.json();

    if (!response.ok) {
      $("loginMessage").textContent = data.detail || "Login failed.";
      return;
    }

    token = data.access_token;
    localStorage.setItem("clinicflow_token", token);
    $("loginMessage").textContent = "";
    showDashboard();
    showToast("Welcome back.");
  } catch {
    $("loginMessage").textContent = "Could not connect to the server.";
  }
}

function showDashboard() {
  $("loginBox").classList.add("hidden");
  $("dashboard").classList.remove("hidden");
  loadDoctors();
  loadAppointments();
}

function logout() {
  token = "";
  localStorage.removeItem("clinicflow_token");
  $("dashboard").classList.add("hidden");
  $("loginBox").classList.remove("hidden");
  showToast("Logged out.");
}

async function loadDoctors() {
  try {
    const response = await fetch(`${API}/doctors`);
    const doctors = await response.json();

    if (!response.ok || !Array.isArray(doctors)) return;

    const doctorSelect = $("doctorSelect");
    const scheduleDoctor = $("scheduleDoctor");
    const landing = $("landingDoctors");

    doctorSelect.innerHTML = "";
    scheduleDoctor.innerHTML = "";

    doctors.forEach((doctor, index) => {
      const option = document.createElement("option");
      option.value = doctor.id;
      option.textContent = `${doctor.name} — ${doctor.specialization}`;
      doctorSelect.appendChild(option);
      scheduleDoctor.appendChild(option.cloneNode(true));
    });

    landing.innerHTML = doctors.slice(0, 6).map((doctor, index) => {
      const initials = doctor.name.split(/\s+/).slice(-2).map(x => x[0]).join("").toUpperCase();
      return `
        <article class="doctor-card">
          <div class="doctor-photo">${initials || "DR"}</div>
          <div>
            <strong>${escapeHtml(doctor.name)}</strong>
            <small>${escapeHtml(doctor.specialization || "Doctor")}</small>
          </div>
          <span class="doctor-status">Available</span>
        </article>`;
    }).join("");

    if (!doctors.length) {
      landing.innerHTML = `<div class="doctor-card"><strong>No doctors found.</strong></div>`;
    }
  } catch {
    $("landingDoctors").innerHTML = `<div class="doctor-card"><strong>Doctors could not be loaded.</strong></div>`;
  }
}

async function bookAppointment() {
  const doctor_id = Number($("doctorSelect").value);
  const appointment_date = $("appointmentDate").value;
  const start_time = $("startTime").value;
  const end_time = $("endTime").value;

  if (!doctor_id || !appointment_date || !start_time || !end_time) {
    $("bookingMessage").textContent = "Complete all appointment fields.";
    return;
  }

  if (start_time >= end_time) {
    $("bookingMessage").textContent = "End time must be after start time.";
    return;
  }

  try {
    const response = await fetch(`${API}/appointments`, {
      method: "POST",
      headers: apiHeaders(),
      body: JSON.stringify({ doctor_id, appointment_date, start_time, end_time })
    });
    const data = await response.json();

    if (!response.ok) {
      $("bookingMessage").textContent = data.detail || "Booking failed.";
      showToast(data.detail || "Booking failed.");
      return;
    }

    $("bookingMessage").textContent = "Appointment booked successfully.";
    showToast("Appointment booked.");
    loadAppointments();
    loadSchedule();
  } catch {
    $("bookingMessage").textContent = "Could not connect to the server.";
  }
}

async function loadAppointments() {
  if (!token) return;

  try {
    const response = await fetch(`${API}/appointments?page=1&limit=10&sort_by=appointment_date&order=asc`, {
      headers: apiHeaders()
    });

    if (response.status === 401) {
      logout();
      return;
    }

    const data = await response.json();
    if (!response.ok) return;

    const items = data.items || [];
    const container = $("appointmentsResults");

    if (!items.length) {
      container.innerHTML = `<div class="result-item muted">No appointments found.</div>`;
      return;
    }

    container.innerHTML = items.map(appointment => {
      const cancelled = appointment.status === "cancelled";
      return `
        <div class="appointment-item">
          <div><strong>${escapeHtml(appointment.patient_name || "Patient")}</strong><small>${escapeHtml(appointment.doctor_name || "Doctor")}</small></div>
          <div><strong>${escapeHtml(appointment.appointment_date)}</strong><small>${escapeHtml(appointment.start_time)} – ${escapeHtml(appointment.end_time)}</small></div>
          <span class="status ${cancelled ? "cancelled" : ""}">${escapeHtml(appointment.status || "booked")}</span>
          ${cancelled
            ? `<small>Fee: ₹${Number(appointment.cancellation_fee || 0)}</small>`
            : `<button class="cancel-btn" onclick="cancelAppointment(${appointment.id})">Cancel</button>`}
        </div>`;
    }).join("");
  } catch {}
}

async function cancelAppointment(id) {
  if (!confirm("Cancel this appointment?")) return;

  try {
    const response = await fetch(`${API}/appointments/${id}/cancel`, {
      method: "PATCH",
      headers: apiHeaders()
    });
    const data = await response.json();

    if (!response.ok) {
      showToast(data.detail || "Cancellation failed.");
      return;
    }

    showToast(`Cancelled. Fee: ₹${Number(data.cancellation_fee || 0)}`);
    loadAppointments();
  } catch {
    showToast("Could not connect to the server.");
  }
}

async function searchAppointments() {
  const name = $("searchName").value.trim();
  if (!name) {
    $("searchResults").innerHTML = `<div class="result-item muted">Enter a patient name.</div>`;
    return;
  }

  try {
    const response = await fetch(`${API}/appointments/search?patientName=${encodeURIComponent(name)}&page=1&limit=10`, {
      headers: apiHeaders()
    });
    const data = await response.json();

    if (!response.ok) {
      $("searchResults").innerHTML = `<div class="result-item">${escapeHtml(data.detail || "Search failed.")}</div>`;
      return;
    }

    const items = data.items || [];
    $("searchResults").innerHTML = items.length
      ? items.map(a => `
          <div class="result-item">
            <strong>${escapeHtml(a.patient_name || "Patient")}</strong> · ${escapeHtml(a.doctor_name || "Doctor")}
            <br><span class="muted">${escapeHtml(a.appointment_date)} · ${escapeHtml(a.start_time)}–${escapeHtml(a.end_time)} · ${escapeHtml(a.status || "")}</span>
          </div>`).join("")
      : `<div class="result-item muted">No appointments found for "${escapeHtml(name)}".</div>`;
  } catch {
    $("searchResults").innerHTML = `<div class="result-item">Could not connect to the server.</div>`;
  }
}

async function loadSchedule() {
  const doctor = $("scheduleDoctor").value;
  const date = $("scheduleDate").value;

  if (!doctor || !date) {
    $("scheduleResults").innerHTML = `<div class="result-item muted">Select a doctor and date.</div>`;
    return;
  }

  try {
    const response = await fetch(`${API}/doctors/${doctor}/appointments?appointment_date=${encodeURIComponent(date)}`, {
      headers: apiHeaders()
    });
    const data = await response.json();

    if (!response.ok) {
      $("scheduleResults").innerHTML = `<div class="result-item">${escapeHtml(data.detail || "Could not load schedule.")}</div>`;
      return;
    }

    const items = data.appointments || [];
    $("scheduleResults").innerHTML = `
      <div class="result-item"><strong>${escapeHtml(data.doctor?.name || "Doctor")}</strong> · ${escapeHtml(data.date || date)}</div>
      ${items.length
        ? items.map(a => `<div class="result-item"><strong>${escapeHtml(a.start_time)} – ${escapeHtml(a.end_time)}</strong> · ${escapeHtml(a.patient_name || "Patient")} <span class="muted">· ${escapeHtml(a.status || "")}</span></div>`).join("")
        : `<div class="result-item muted">No appointments for this day.</div>`}`;
  } catch {
    $("scheduleResults").innerHTML = `<div class="result-item">Could not connect to the server.</div>`;
  }
}

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, ch => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
  }[ch]));
}

$("registerBtn").addEventListener("click", register);
$("loginBtn").addEventListener("click", login);
$("logoutBtn").addEventListener("click", logout);
$("bookBtn").addEventListener("click", bookAppointment);
$("searchBtn").addEventListener("click", searchAppointments);
$("scheduleBtn").addEventListener("click", loadSchedule);
$("refreshBtn").addEventListener("click", loadAppointments);

["loginPassword", "registerPassword"].forEach(id => {
  $(id).addEventListener("keydown", e => {
    if (e.key === "Enter") login();
  });
});

const today = new Date();
const localDate = new Date(today.getTime() - today.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
$("appointmentDate").value = localDate;
$("scheduleDate").value = localDate;

if (token) showDashboard();
loadDoctors();
