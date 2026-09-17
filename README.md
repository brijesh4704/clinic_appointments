````markdown
<div align="center">

<img src="https://img.shields.io/badge/-%F0%9F%8F%A5%20CLINICFLOW-2563EB?style=for-the-badge&labelColor=0a0a0a&color=2563EB" alt="ClinicFlow" height="50"/>

# ClinicFlow — Conflict-Free Clinic Appointment Management

### *Appointments that stay conflict-free.*

<p>
A full-stack clinic appointment management system designed to help front-desk staff book, manage, search, reschedule, and track appointments without double-booking doctors.
</p>

<br/>

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.x-009688?style=flat-square&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=flat-square&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-Frontend-E34F26?style=flat-square&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-Styling-1572B6?style=flat-square&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-Frontend-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=flat-square&logo=github&logoColor=white)

<br/>

> **Built for busy clinics** — ClinicFlow focuses on the most important appointment-management requirement: **a doctor should never be double-booked.**

</div>

---

## 📋 Table of Contents

- [🌟 Why ClinicFlow?](#-why-clinicflow)
- [✨ Features](#-features)
- [🔄 Appointment Lifecycle](#-appointment-lifecycle)
- [🧩 Twists & Automation](#-twists--automation)
- [📸 Screenshots](#-screenshots)
- [🛠 Tech Stack](#-tech-stack)
- [📁 Project Structure](#-project-structure)
- [⚙️ Installation & Setup](#️-installation--setup)
- [🔐 Authentication](#-authentication)
- [🔌 API Reference](#-api-reference)
- [⏰ Clock & Automation](#-clock--automation)
- [🔔 Notification Outbox](#-notification-outbox)
- [🧪 Testing](#-testing)
- [🗄️ Database Design](#️-database-design)
- [🔒 Business Rules](#-business-rules)
- [🔮 Future Roadmap](#-future-roadmap)
- [🐛 Troubleshooting](#-troubleshooting)
- [👨‍💻 Author](#-author)
- [📄 License](#-license)

---

# 🌟 Why ClinicFlow?

Busy clinic front desks often have to manage appointments manually while handling patients, doctors, cancellations, and schedule changes at the same time.

This can result in:

- ❌ Double-booked doctors
- ❌ Conflicting appointment times
- ❌ Difficulty finding patient appointments
- ❌ Manual schedule checking
- ❌ Unclear cancellation charges
- ❌ Missed appointments
- ❌ Lack of appointment reminders

ClinicFlow provides a centralized system for managing these problems.

| Problem | ClinicFlow Solution |
|---|---|
| ❌ Doctor double-booking | 🔒 Backend conflict detection |
| 🔄 Appointment changes | 📅 Conflict-free rescheduling |
| 🔎 Difficult patient lookup | 👤 Patient name search |
| 🩺 Manual doctor schedule | 📋 Daily doctor schedule |
| 💰 Unclear cancellation rules | 💵 Cancellation fee tracking |
| 🔔 Patients forget appointments | 📢 Notification Service + outbox |
| 🚫 Missed appointments | ⏱️ Automatic no-show detection |
| 📊 Large appointment lists | 📄 Pagination & sorting |
| 🔐 Unauthorized access | 🔑 Authentication |

---

# ✨ Features

## 🧑‍💼 Front Desk Management

- **Appointment Booking** — Create appointments for patients with selected doctors.
- **Conflict Detection** — Prevent overlapping appointments for the same doctor.
- **Doctor Schedule** — View a doctor's appointments for a selected date.
- **Patient Search** — Find appointments using the patient's name.
- **Appointment Management** — View, cancel, reschedule, and complete appointments.
- **Pagination** — Handle large appointment lists efficiently.
- **Sorting** — Sort appointments by supported fields and order.

---

## 📅 Conflict-Free Booking

ClinicFlow checks appointment conflicts before saving a booking.

Example:

```text
Doctor: Dr. Sharma

10:00 ───────── 11:00    Patient A
10:30 ───────── 11:30    Patient B
                         ❌ Conflict
````

Back-to-back appointments are allowed:

```text
10:00 ───────── 10:30    Patient A
10:30 ───────── 11:00    Patient B
                         ✅ Allowed
```

The backend performs the conflict check before creating or rescheduling an appointment.

### Conflict Rule

For two appointments belonging to the same doctor:

```text
newStart < existingEnd
AND
newEnd > existingStart
```

If both conditions are true, the appointments overlap.

---

# 🔄 Appointment Lifecycle

```text
                     ┌──────────────┐
                     │    BOOKED    │
                     └──────┬───────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
         COMPLETED      CANCELLED     RESCHEDULE
                                          │
                                          ▼
                                   Check Availability
                                          │
                                    ┌─────┴─────┐
                                    ▼           ▼
                                Available    Conflict
                                    │           │
                                    ▼           ▼
                                Update       Reject


BOOKED
   │
   │ Start + 30 minutes
   ▼
Not Completed
   │
   ▼
NO-SHOW
```

---

# 🔄 T6 — Appointment Rescheduling

ClinicFlow supports safe appointment rescheduling.

A rescheduled appointment must:

* Keep the **same patient**
* Keep the **same doctor**
* Use the requested new date/time
* Re-check doctor availability
* Reject the operation if the new time overlaps another appointment

### Example

```text
Current Appointment

Patient: Rahul Sharma
Doctor: Dr. Sharma
Time: 10:00 – 10:30

             ↓

        RESCHEDULE

             ↓

New Time:
11:00 – 11:30

             ↓

Check Doctor Availability

             ↓

       ┌───────────────┐
       │ Available?    │
       └───────┬───────┘
               │
        ┌──────┴──────┐
        ▼             ▼
       YES            NO
        │             │
        ▼             ▼
    Reschedule     Reject
```

If another appointment exists from `11:15 – 11:45`, the requested `11:00 – 11:30` slot is rejected.

The patient and doctor remain unchanged.

---

# 📢 T1 — Morning Appointment Reminders

ClinicFlow integrates a **Notification Service** for daily appointment reminders.

Each morning, the system identifies appointments scheduled for that day and generates reminder notifications for patients.

The workflow is:

```text
                 POST /clock
                      │
                      ▼
              Current Clinic Date
                      │
                      ▼
             Today's Appointments
                      │
                      ▼
             Notification Service
                      │
                      ▼
                  /outbox
```

### Example

Today's appointments:

```text
10:00 AM   Rahul Sharma   Dr. Sharma
11:00 AM   Priya Singh    Dr. Mehta
```

After:

```http
POST /clock
```

the Notification Service generates reminder entries.

Check them using:

```http
GET /outbox
```

Example:

```json
{
  "type": "appointment_reminder",
  "appointment_id": 12,
  "patient_id": 4,
  "message": "Reminder: You have an appointment today at 10:00 AM with Dr. Sharma."
}
```

---

# ⏱️ T2 — Automatic No-Show Detection

ClinicFlow automatically marks an appointment as **NO-SHOW** when:

```text
Appointment Start Time + 30 minutes
```

has passed and the appointment has not been completed.

### No-Show Workflow

```text
Appointment Start
       │
       ▼
10:00 AM
       │
       │ + 30 minutes
       ▼
10:30 AM
       │
       ▼
POST /clock
       │
       ▼
Check Status
       │
   ┌───┴────┐
   ▼        ▼
Completed  Not Completed
   │        │
   ▼        ▼
 Keep     NO-SHOW
```

### Completed Appointment

```text
10:00 AM → Appointment starts
10:20 AM → Doctor completes appointment
10:30 AM → POST /clock

Result: ✅ COMPLETED
```

### Missed Appointment

```text
10:00 AM → Appointment starts
10:30 AM → POST /clock
            Appointment not completed

Result: 🚫 NO-SHOW
```

---

# 🧩 Twists & Automation

## Level 1 — T6: Lifecycle

**Reschedule an appointment to a new time while maintaining the same patient and doctor and re-checking appointment conflicts.**

Endpoint:

```http
PUT /appointments/{appointment_id}/reschedule
```

---

## Level 2 — T1: Integrate

**Each morning, remind patients of today's appointments through the Notification Service.**

Triggered by:

```http
POST /clock
```

Verified through:

```http
GET /outbox
```

---

## Level 3 — T2: Automation

**Automatically mark appointments as no-show 30 minutes after their start time if they have not been completed.**

Triggered by:

```http
POST /clock
```

---

# 📸 Screenshots

Add screenshots of the deployed application here.

### 📊 Dashboard

```markdown
![ClinicFlow Dashboard](screenshots/dashboard.png)
```

### 📅 Appointments

```markdown
![Appointments](screenshots/appointments.png)
```

### 👨‍⚕️ Doctors

```markdown
![Doctors](screenshots/doctors.png)
```

### 👥 Patients

```markdown
![Patients](screenshots/patients.png)
```

### 🗓️ Doctor Schedule

```markdown
![Doctor Schedule](screenshots/doctor-schedule.png)
```

### 🔄 Reschedule Appointment

```markdown
![Reschedule Appointment](screenshots/reschedule.png)
```

### 🔔 Notification Outbox

```markdown
![Notification Outbox](screenshots/outbox.png)
```

---

# 🛠 Tech Stack

## Backend

| Technology     | Role                         |
| -------------- | ---------------------------- |
| **Python**     | Backend programming language |
| **FastAPI**    | REST API framework           |
| **SQLAlchemy** | Database ORM                 |
| **SQLite**     | Relational database          |
| **Pydantic**   | Request/response validation  |
| **Uvicorn**    | ASGI server                  |

## Frontend

| Technology     | Role                                        |
| -------------- | ------------------------------------------- |
| **HTML5**      | Application structure                       |
| **CSS3**       | Responsive styling                          |
| **JavaScript** | Frontend interactions and API communication |

## Development

| Tool                | Role                          |
| ------------------- | ----------------------------- |
| **Git**             | Version control               |
| **GitHub**          | Source-code hosting           |
| **FastAPI Swagger** | API testing and documentation |

---

# 📁 Project Structure

```text
ClinicFlow/
│
├── main.py
├── requirements.txt
├── README.md
│
├── static/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── models/
│   └── ...
│
├── schemas/
│   └── ...
│
├── services/
│   └── ...
│
├── database/
│   └── ...
│
└── tests/
    └── ...
```

### Main Components

| Component   | Responsibility                     |
| ----------- | ---------------------------------- |
| `main.py`   | FastAPI application and API routes |
| `models/`   | Database models                    |
| `schemas/`  | Request/response validation        |
| `services/` | Business and notification logic    |
| `static/`   | Dashboard and frontend             |
| `tests/`    | Automated/API tests                |

---

# ⚙️ Installation & Setup

## Prerequisites

* Python `3.9+`
* pip
* Git
* Modern web browser

---

## Step 1 — Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/ClinicFlow.git
cd ClinicFlow
```

---

## Step 2 — Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 4 — Start Application

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

FastAPI Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🔐 Authentication

ClinicFlow uses authenticated access for protected clinic operations.

Authentication helps ensure that appointment-management operations are performed only by authorized users.

> Update this section with the exact authentication mechanism if additional authentication is added to the final deployment.

---

# 🔌 API Reference

## 📅 Appointment APIs

| Method | Endpoint        | Description        |
| ------ | --------------- | ------------------ |
| `GET`  | `/appointments` | List appointments  |
| `POST` | `/appointments` | Create appointment |
| `GET`  | `               |                    |
