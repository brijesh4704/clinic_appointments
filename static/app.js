const API = "";

let token = localStorage.getItem("clinicflow_token");


function headers() {

    const h = {
        "Content-Type": "application/json"
    };

    if (token) {
        h["Authorization"] = "Bearer " + token;
    }

    return h;
}


// ============================================================
// LANDING PAGE
// ============================================================

function showApp() {

    document
        .getElementById("app")
        .classList.remove("hidden");

    document
        .getElementById("app")
        .scrollIntoView({
            behavior: "smooth"
        });

    if (token) {
        showDashboard();
    }
}


// ============================================================
// REGISTER
// ============================================================

async function register() {

    const name =
        document.getElementById("registerName").value;

    const email =
        document.getElementById("registerEmail").value;

    const password =
        document.getElementById("registerPassword").value;


    const response = await fetch(
        API + "/auth/register",
        {
            method: "POST",
            headers: headers(),
            body: JSON.stringify({
                name,
                email,
                password
            })
        }
    );


    const data = await response.json();

    document.getElementById(
        "registerMessage"
    ).textContent =
        response.ok
            ? "Registration successful. You can now login."
            : data.detail;
}


// ============================================================
// LOGIN
// ============================================================

async function login() {

    const email =
        document.getElementById("loginEmail").value;

    const password =
        document.getElementById("loginPassword").value;


    const response = await fetch(
        API + "/auth/login",
        {
            method: "POST",
            headers: headers(),
            body: JSON.stringify({
                email,
                password
            })
        }
    );


    const data = await response.json();


    if (!response.ok) {

        document.getElementById(
            "loginMessage"
        ).textContent = data.detail;

        return;
    }


    token = data.access_token;

    localStorage.setItem(
        "clinicflow_token",
        token
    );

    showDashboard();
}


// ============================================================
// SHOW DASHBOARD
// ============================================================

function showDashboard() {

    document
        .getElementById("loginBox")
        .classList.add("hidden");

    document
        .getElementById("dashboard")
        .classList.remove("hidden");

    loadDoctors();

    loadAppointments();
}


// ============================================================
// LOGOUT
// ============================================================

function logout() {

    token = null;

    localStorage.removeItem(
        "clinicflow_token"
    );

    document
        .getElementById("dashboard")
        .classList.add("hidden");

    document
        .getElementById("loginBox")
        .classList.remove("hidden");
}


// ============================================================
// DOCTORS
// ============================================================

async function loadDoctors() {

    const response = await fetch(
        API + "/doctors"
    );

    const doctors = await response.json();


    const doctorSelect =
        document.getElementById("doctorSelect");

    const scheduleDoctor =
        document.getElementById("scheduleDoctor");


    doctorSelect.innerHTML = "";
    scheduleDoctor.innerHTML = "";


    doctors.forEach(doctor => {

        const option =
            document.createElement("option");

        option.value = doctor.id;

        option.textContent =
            doctor.name +
            " - " +
            doctor.specialization;

        doctorSelect.appendChild(option);


        const option2 =
            option.cloneNode(true);

        scheduleDoctor.appendChild(option2);
    });
}


// ============================================================
// BOOK APPOINTMENT
// ============================================================

async function bookAppointment() {

    const doctor_id =
        Number(
            document.getElementById(
                "doctorSelect"
            ).value
        );

    const appointment_date =
        document.getElementById(
            "appointmentDate"
        ).value;

    const start_time =
        document.getElementById(
            "startTime"
        ).value;

    const end_time =
        document.getElementById(
            "endTime"
        ).value;


    const response = await fetch(
        API + "/appointments",
        {
            method: "POST",
            headers: headers(),

            body: JSON.stringify({
                doctor_id,
                appointment_date,
                start_time,
                end_time
            })
        }
    );


    const data = await response.json();


    document.getElementById(
        "bookingMessage"
    ).textContent =
        response.ok
            ? "Appointment booked successfully."
            : data.detail;


    if (response.ok) {
        loadAppointments();
        loadSchedule();
    }
}


// ============================================================
// LOAD APPOINTMENTS
// ============================================================

async function loadAppointments() {

    if (!token) return;


    const response = await fetch(
        API +
        "/appointments?page=1&limit=10&sort_by=appointment_date&order=asc",
        {
            headers: headers()
        }
    );


    if (!response.ok) return;


    const data = await response.json();

    const container =
        document.getElementById(
            "appointmentsResults"
        );


    container.innerHTML = "";


    data.items.forEach(
        appointment => {

            const card =
                document.createElement("div");

            card.className =
                "appointment-card";


            card.innerHTML = `
                <strong>${appointment.patient_name}</strong>
                <br>
                ${appointment.doctor_name}
                <br>
                ${appointment.appointment_date}
                |
                ${appointment.start_time}
                -
                ${appointment.end_time}
                <br>
                Status:
                ${appointment.status}
                <br>
                ${
                    appointment.status === "booked"
                    ? `<button
                         class="cancel-btn"
                         onclick="cancelAppointment(${appointment.id})">
                         Cancel
                       </button>`
                    : `Cancellation fee: ₹${appointment.cancellation_fee}`
                }
            `;


            container.appendChild(card);
        }
    );
}


// ============================================================
// CANCEL
// ============================================================

async function cancelAppointment(id) {

    const response = await fetch(
        API +
        "/appointments/" +
        id +
        "/cancel",
        {
            method: "PATCH",
            headers: headers()
        }
    );


    const data = await response.json();


    alert(
        response.ok
            ? "Appointment cancelled. Fee: ₹" +
              data.cancellation_fee
            : data.detail
    );


    if (response.ok) {
        loadAppointments();
    }
}


// ============================================================
// SEARCH
// ============================================================

async function searchAppointments() {

    const name =
        document.getElementById(
            "searchName"
        ).value;


    if (!name) return;


    const response = await fetch(
        API +
        "/appointments/search?patientName=" +
        encodeURIComponent(name) +
        "&page=1&limit=10",
        {
            headers: headers()
        }
    );


    const data = await response.json();


    const container =
        document.getElementById(
            "searchResults"
        );


    container.innerHTML = "";


    data.items.forEach(
        appointment => {

            const card =
                document.createElement("div");

            card.className =
                "appointment-card";


            card.innerHTML = `
                <strong>
                    ${appointment.patient_name}
                </strong>
                <br>
                ${appointment.doctor_name}
                <br>
                ${appointment.appointment_date}
                |
                ${appointment.start_time}
                -
                ${appointment.end_time}
                <br>
                Status:
                ${appointment.status}
            `;


            container.appendChild(card);
        }
    );


    if (data.items.length === 0) {

        container.innerHTML =
            "<p>No appointments found.</p>";
    }
}


// ============================================================
// DOCTOR SCHEDULE
// ============================================================

async function loadSchedule() {

    const doctor =
        document.getElementById(
            "scheduleDoctor"
        ).value;

    const date =
        document.getElementById(
            "scheduleDate"
        ).value;


    if (!doctor || !date) return;


    const response = await fetch(
        API +
        `/doctors/${doctor}/appointments?appointment_date=${date}`,
        {
            headers: headers()
        }
    );


    const data = await response.json();


    const container =
        document.getElementById(
            "scheduleResults"
        );


    container.innerHTML =
        `<h4>
            ${data.doctor.name}
            — ${data.date}
         </h4>`;


    data.appointments.forEach(
        appointment => {

            container.innerHTML += `
                <div class="appointment-card">
                    ${appointment.start_time}
                    -
                    ${appointment.end_time}
                    <br>
                    <strong>
                        ${appointment.patient_name}
                    </strong>
                    <br>
                    ${appointment.status}
                </div>
            `;
        }
    );


    if (data.appointments.length === 0) {

        container.innerHTML +=
            "<p>No appointments for this day.</p>";
    }
}


// ============================================================
// STARTUP
// ============================================================

if (token) {
    showApp();
}