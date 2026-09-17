WeCare-Doctor_Appointment_Booking_Application-main.zip
Zip Archive
is this correct according to problem statement
Prescripto-main.zip
Zip Archive
is this correct
clinicflow.zip
Zip Archive
is this correct
Pasted code(6).py
Python
Prescripto-main(1).zip
Zip Archive
take help from this project to change the frontent and design
Pasted code.js
JavaScript
Pasted code(7).py
Python
add final changes
Pasted markdown(3).md
File

Absolutely. For the Auriga IT Builder assessment, your README should look like a real product README and clearly document the UI, backend, database, APIs, conflict-free booking, rescheduling, reminders, cancellation fees, and no-show automation.

You can replace your current README.md with this:

# ClinicFlow 🏥

### Conflict-Free Clinic Appointment Management System

ClinicFlow is a full-stack clinic appointment management system designed for busy clinic front desks.

It solves a common clinic problem: **doctor double-booking and difficult appointment management**.

The system allows staff to register patients, manage doctors, book appointments, prevent overlapping appointments, reschedule appointments safely, search patient appointments, view a doctor's daily schedule, handle cancellation fees fairly, send daily appointment reminders through a notification outbox, and automatically mark missed appointments as no-show.

---

## 🌐 Project Overview

ClinicFlow provides a simple interface for clinic staff to manage appointments from one place.

### The main problem

A busy clinic may face problems such as:

- Two patients being booked with the same doctor at the same time.
- Patients taking the same available slot.
- Difficulty finding a patient's appointment.
- Manual checking of a doctor's daily schedule.
- Confusion around cancellation charges.
- Missed appointments not being tracked properly.
- Patients not receiving appointment reminders.

### ClinicFlow solution

ClinicFlow provides:

- Conflict-free appointment booking
- Doctor schedule management
- Patient appointment search
- Appointment rescheduling
- Fair cancellation fee handling
- Daily appointment reminders
- Automatic no-show detection
- Appointment completion
- Pagination and sorting
- Secure registration and login

---

# ✨ Key Features

## 1. Conflict-Free Booking

ClinicFlow prevents two appointments for the same doctor from overlapping.

For example:

```text
Doctor: Dr. Sharma

10:00 ───── 11:00  Patient A
10:30 ───── 11:30  Patient B  ❌ Conflict
11:00 ───── 12:00  Patient C  ✅ Allowed

Back-to-back appointments are allowed:

10:00 ───── 11:00  Patient A
11:00 ───── 12:00  Patient B

The backend checks for overlapping appointments before creating or rescheduling an appointment.

2. Appointment Rescheduling

Patients can reschedule an existing appointment to another date and time.

The system:

Finds the existing appointment.
Verifies the logged-in patient owns it.
Checks that the appointment is still active.
Checks the new start/end time.
Re-checks doctor availability.
Rejects the request if the new slot overlaps another appointment.
Keeps the same patient and doctor when rescheduling succeeds.
3. Fair Cancellation Policy

ClinicFlow uses a simple cancellation rule.

Cancellation Time	Fee
24 hours or more before appointment	₹0
Less than 24 hours before appointment	₹200

Example:

Appointment:
September 20, 10:00 AM

Cancelled:
September 18, 10:00 AM

Fee:
₹0

Late cancellation:

Appointment:
September 20, 10:00 AM

Cancelled:
September 19, 12:00 PM

Fee:
₹200

The cancellation fee is calculated by the backend.

4. Patient Appointment Search

The front desk can search for appointments using the patient's name.

Example:

Search: Brijesh

Results:
Brijesh Singh
Dr. Sharma
20 Sep 2026
10:00 - 11:00
Booked

The API supports partial name matching.

5. Doctor Daily Schedule

The front desk can view all appointments for a specific doctor on a selected date.

Example:

Dr. Sharma — 20 September 2026

10:00 - 11:00    Brijesh Singh
11:00 - 12:00    Rahul Kumar
12:00 - 01:00    Priya Sharma

Appointments are returned in time order.

6. Daily Appointment Reminders

ClinicFlow includes a notification outbox for appointment reminders.

The system can run the clock automation:

POST /clock

For today's booked appointments, ClinicFlow creates reminder notifications.

Example:

Reminder:
You have an appointment with Dr. Sharma today at 10:00.

Notifications can be viewed through:

GET /outbox

The outbox represents the integration point for a future external Notification Service such as SMS, email, or WhatsApp.

7. Automatic No-Show Detection

ClinicFlow automatically identifies appointments that were not completed.

If an appointment remains booked for 30 minutes after its start time, it is automatically marked:

no_show

Example:

Appointment:
10:00 AM

Clock:
10:30 AM

Status:
no_show

Completed appointments are not marked as no-show.

8. Appointment Completion

A patient can mark an appointment as completed.

Status changes:

booked → completed

Completed appointments are excluded from the no-show automation.

9. Pagination and Sorting

The appointment listing API supports:

Pagination
Page size
Sorting
Ascending order
Descending order

Example:

GET /appointments?page=1&page_size=10&sort_by=appointment_date&sort_order=asc
🖥️ User Interface

ClinicFlow includes a responsive web interface designed for clinic front-desk staff.

Landing Page

The landing page explains:

What ClinicFlow is
The problem it solves
Key features
Target users
How the system works
Future improvements

The UI uses a clean healthcare-inspired design with:

Responsive navigation
Hero section
Feature cards
Doctor section
Appointment workflow
Statistics
Login/Register interface
Dashboard
Dashboard

After login, users can access the appointment management dashboard.

The dashboard provides:

📅 Book Appointment

Create an appointment by selecting:

Doctor
Appointment date
Start time
End time

The backend automatically checks for conflicts.

🔎 Search Patient

Search appointments by patient name.

👨‍⚕️ Doctor Schedule

Select a doctor and date to view their appointments.

📋 Appointment List

View appointments with:

Patient
Doctor
Date
Time
Status
Cancellation fee
Available actions
❌ Cancel Appointment

Cancel an appointment and automatically calculate the applicable fee.

🔄 Reschedule Appointment

Move an appointment to another time while maintaining:

Same patient
Same doctor
Conflict-free scheduling
✅ Complete Appointment

Mark an active appointment as completed.

🎯 Target Users

ClinicFlow is designed for:

Clinic receptionists
Front-desk staff
Small clinics
Multi-doctor clinics
Appointment coordinators
Patients
🔄 How ClinicFlow Works
                ┌─────────────────┐
                │     Patient     │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ ClinicFlow UI   │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │   REST APIs     │
                │    FastAPI      │
                └────────┬────────┘
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
        ┌────────┐ ┌──────────┐ ┌────────────┐
        │ Users  │ │ Doctors  │ │Appointments│
        └────────┘ └──────────┘ └────────────┘
                         │
                         ▼
                ┌─────────────────┐
                │     SQLite      │
                │    Database     │
                └─────────────────┘
🛠️ Tech Stack
Frontend
HTML5
CSS3
JavaScript
Responsive UI
Fetch API
Backend
Python
FastAPI
Pydantic
Uvicorn
Database
SQLite
SQLAlchemy ORM
Authentication
Token-based authentication
Password hashing
Development
Git
GitHub
VS Code
Swagger/OpenAPI
📁 Project Structure
clinic_appointments/
│
├── main.py
├── clinicflow.db
├── requirements.txt
│
├── README.md
├── REASONING.md
├── AI_LOGS.md
│
├── static/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
└── __pycache__/

__pycache__ should not be committed to GitHub.

⚙️ Installation
1. Clone the repository
git clone https://github.com/brijesh4704/clinic_appointments.git

Move into the project:

cd clinic_appointments
2. Create a virtual environment
Windows
python -m venv venv
venv\Scripts\activate
macOS / Linux
python3 -m venv venv
source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
▶️ Run the Application

Start the FastAPI server:

uvicorn main:app --reload --host 0.0.0.0 --port 8000

The application will be available at:

http://localhost:8000

Open the browser and visit:

http://localhost:8000
📚 API Documentation

FastAPI automatically provides interactive API documentation.

Swagger UI:

http://localhost:8000/docs

ReDoc:

http://localhost:8000/redoc
🔐 Authentication APIs
Register
POST /auth/register

Creates a new user account.

Example:

{
  "name": "Brijesh Singh",
  "email": "brijesh@example.com",
  "password": "password123"
}
Login
POST /auth/login

Returns an authentication token.

👨‍⚕️ Doctor APIs
Get Doctors
GET /doctors

Returns the available doctors.

Create Doctor
POST /doctors

Creates a new doctor.

Example:

{
  "name": "Dr. Sharma",
  "specialization": "General Physician"
}
📅 Appointment APIs
Create Appointment
POST /appointments

Creates an appointment after checking for doctor conflicts.

Get Appointments
GET /appointments

Supports pagination and sorting.

Example:

GET /appointments?page=1&page_size=10&sort_by=appointment_date&sort_order=asc
Get Appointment
GET /appointments/{appointment_id}

Returns a single appointment.

Search Patient Appointments
GET /appointments/search?patientName=Brijesh

Searches appointments using the patient's name.

Doctor Daily Schedule
GET /doctors/{doctor_id}/appointments?appointment_date=2026-09-20

Returns appointments for a doctor on a specific date.

Cancel Appointment
PATCH /appointments/{appointment_id}/cancel

Cancels an appointment and calculates the cancellation fee.

Reschedule Appointment
PATCH /appointments/{appointment_id}/reschedule

Example:

{
  "appointment_date": "2026-09-20",
  "start_time": "14:00",
  "end_time": "15:00"
}

The new slot is checked for conflicts before updating the appointment.

Complete Appointment
PATCH /appointments/{appointment_id}/complete

Marks a booked appointment as completed.

🔔 Notification APIs
Run Clock Automation
POST /clock

Runs the appointment automation.

It performs:

Today's appointment reminder creation.
No-show detection.

Optional request:

{
  "now": "2026-09-20T10:30:00"
}

The optional now value makes the automation deterministic and easier to test.

View Notification Outbox
GET /outbox

Returns generated appointment reminder notifications.

Example:

{
  "appointment_id": 1,
  "patient_id": 2,
  "message": "Reminder: You have an appointment with Dr. Sharma today at 10:00."
}
🧪 Testing the Core Rules
Test 1 — Normal Booking
10:00 - 11:00

Expected:

200 OK
Test 2 — Overlapping Booking

Existing:

10:00 - 11:00

New:

10:30 - 11:30

Expected:

409 Conflict
Test 3 — Back-to-Back Booking

Existing:

10:00 - 11:00

New:

11:00 - 12:00

Expected:

200 OK

Back-to-back appointments are allowed.

Test 4 — Reschedule Conflict

Existing:

Patient A
10:00 - 11:00

Another appointment:

Patient B
14:00 - 15:00

Attempt to reschedule Patient A:

14:30 - 15:30

Expected:

409 Conflict
Test 5 — Valid Reschedule

Reschedule Patient A to:

12:00 - 13:00

Expected:

200 OK

The patient and doctor remain unchanged.

Test 6 — Early Cancellation

Cancellation occurs 24 hours or more before appointment.

Expected:

Fee = ₹0
Test 7 — Late Cancellation

Cancellation occurs less than 24 hours before appointment.

Expected:

Fee = ₹200
Test 8 — Daily Reminder

Run:

POST /clock

for a day containing booked appointments.

Expected:

reminders_created >= 1

Then:

GET /outbox

should show the reminder.

Test 9 — No-Show

Appointment:

10:00 AM

Run:

POST /clock

with:

{
  "now": "2026-09-20T10:30:00"
}

Expected:

status = "no_show"

Before 30 minutes:

10:29 AM → booked

At 30 minutes:

10:30 AM → no_show
🗄️ Database Schema

ClinicFlow uses SQLite with SQLAlchemy.

Main entities:

User
 │
 └────────────── Appointment
                       │
                       │
                    Doctor
User

Stores:

User ID
Name
Email
Password information
Doctor

Stores:

Doctor ID
Doctor name
Specialization
Appointment

Stores:

Appointment ID
Doctor
Patient
Date
Start time
End time
Status
Cancellation fee
Creation time
NotificationOutbox

Stores:

Notification ID
Appointment ID
Patient ID
Message
Creation time
Sent status
🔒 Business Rules

ClinicFlow enforces the following rules at the backend level.

Rule 1 — No Doctor Overlap

Two booked appointments for the same doctor cannot overlap.

The overlap condition is:

existing.start < new.end
AND
existing.end > new.start
Rule 2 — Back-to-Back Slots Allowed
Existing: 10:00 - 11:00
New:      11:00 - 12:00

This is valid.

Rule 3 — Rescheduling Rechecks Availability

Every reschedule request performs the same overlap validation as a new booking.

Rule 4 — Cancellation Fee
>= 24 hours → ₹0
< 24 hours  → ₹200
Rule 5 — No-Show

A booked appointment becomes:

no_show

30 minutes after its start time if it has not been completed or cancelled.

Rule 6 — Completed Appointments

Completed appointments are not converted into no-show.

Rule 7 — Reminder Deduplication

ClinicFlow creates at most one reminder notification for an appointment in the outbox.

🚀 Demo Data

For quick testing, ClinicFlow provides:

POST /demo/seed

This can be used to create demonstration doctors and appointment data.

🧭 UI Workflow
Open ClinicFlow
      │
      ▼
Register / Login
      │
      ▼
Dashboard
      │
      ├── Book Appointment
      │       │
      │       ▼
      │   Conflict Check
      │
      ├── Search Patient
      │
      ├── Doctor Schedule
      │
      ├── Reschedule
      │       │
      │       ▼
      │   Conflict Check
      │
      ├── Cancel
      │       │
      │       ▼
      │   Calculate Fee
      │
      └── Complete Appointment
🔮 Future Features

The following features can be added in future versions:

1. SMS / WhatsApp Reminders

Connect the notification outbox to an external notification provider.

2. Online Payments

Allow patients to pay cancellation fees and consultation charges online.

3. Doctor Availability

Allow doctors to define:

Working hours
Breaks
Holidays
Leave
Available appointment slots
🧠 Design Decisions

ClinicFlow prioritizes the most important requirement first:

A doctor must never be double-booked.

Therefore, conflict validation is performed in the backend instead of relying only on the frontend.

The frontend provides a convenient user experience, but the backend remains responsible for enforcing business rules.

The notification outbox provides a simple integration boundary for future external notification services without coupling the appointment system directly to an SMS or email provider.

The /clock endpoint allows time-based automation to be triggered deterministically during testing.

🐛 Debugging

If the server does not start:

python -m py_compile main.py

Then run:

uvicorn main:app --reload --host 0.0.0.0 --port 8000

Check the API documentation:

http://localhost:8000/docs

If the database needs to be reset during development, stop the server and remove:

clinicflow.db

Then restart the application.

📦 Requirements

Install all dependencies using:

pip install -r requirements.txt

The application requires Python 3 and the packages listed in requirements.txt.

👨‍💻 Author

Brijesh Singh

B.Tech — Computer Science & Data Science

Swami Keshvanand Institute of Technology, Management & Gramothan (SKIT), Jaipur

📄 Assessment Documentation

This repository also contains:

REASONING.md

Documents:

Problem understanding
Architecture decisions
Business rules
Testing approach
Bugs encountered
Fixes implemented
AI_LOGS.md

Contains the complete AI conversation used during development, as required by the assessment.

📌 Project Status
✅ User Registration
✅ User Login
✅ Doctor Management
✅ Appointment Booking
✅ Conflict Detection
✅ Back-to-Back Appointments
✅ Appointment Search
✅ Doctor Daily Schedule
✅ Cancellation Fee
✅ Appointment Rescheduling
✅ Appointment Completion
✅ Daily Reminder Outbox
✅ Automatic No-Show Detection
✅ Pagination
✅ Sorting
✅ Responsive UI
✅ REST APIs
✅ SQLite Database
✅ Swagger Documentation
⭐ ClinicFlow
Appointments that stay conflict-free.

Built to help clinic front desks manage appointments without double-booking doctors.


### One important thing before you push

Because this is for the **Builder assessment**, I would also add a `.gitignore` so you don't push `__pycache__` or your local SQLite database accidentally:

```gitignore
__pycache__/
*.py[cod]
*.db
.venv/
venv/
.env
.DS_Store

Then:

git add README.md .gitignore
git commit -m "Improve project documentation and README"
git push origin main

Don't modify AI_LOGS.md to make it look cleaner—the assessment specifically requires the AI conversation to be pasted there as-is.

ready to paste

Yes — copy everything below directly into your README.md:

# ClinicFlow 🏥

## Conflict-Free Clinic Appointment Management System

ClinicFlow is a full-stack clinic appointment management system built for busy clinic front desks.

It solves a common clinic problem: **doctor double-booking and difficult appointment management**.

The system allows staff to register patients, manage doctors, book appointments, prevent overlapping appointments, reschedule appointments safely, search patient appointments, view a doctor's daily schedule, handle cancellation fees fairly, generate daily appointment reminders, and automatically mark missed appointments as no-show.

---

## 🌐 Project Overview

### The Problem

A busy clinic may face problems such as:

- Two patients being booked with the same doctor at the same time.
- Multiple patients trying to take the same slot.
- Difficulty finding a patient's appointment.
- Difficulty viewing a doctor's complete daily schedule.
- Confusion around cancellation charges.
- Missed appointments not being tracked.
- Patients not receiving appointment reminders.

### The Solution

ClinicFlow provides:

- ✅ Conflict-free appointment booking
- ✅ Doctor daily schedule
- ✅ Patient appointment search
- ✅ Appointment rescheduling
- ✅ Fair cancellation fee handling
- ✅ Daily appointment reminders
- ✅ Automatic no-show detection
- ✅ Appointment completion
- ✅ Pagination and sorting
- ✅ User registration and login
- ✅ Responsive web UI
- ✅ REST APIs

---

# 🖥️ User Interface

ClinicFlow provides a clean and responsive web interface designed for clinic front-desk staff.

### Landing Page

The landing page explains:

- What ClinicFlow is
- The problem it solves
- Key features
- Target users
- How the system works
- Future features

The interface includes:

- Modern healthcare-inspired design
- Responsive navigation
- Hero section
- Feature cards
- Doctor section
- Appointment workflow
- Login/Register
- Appointment dashboard
- Search and schedule tools

### Dashboard

After login, users can:

- Book an appointment
- View appointments
- Search patients
- View a doctor's daily schedule
- Reschedule appointments
- Cancel appointments
- Complete appointments
- View appointment status and cancellation fees

---

# ✨ Key Features

## 1. Conflict-Free Appointment Booking

ClinicFlow prevents two appointments for the same doctor from overlapping.

Example:

```text
Doctor: Dr. Sharma

10:00 - 11:00   Patient A
10:30 - 11:30   Patient B  ❌ Conflict
11:00 - 12:00   Patient C  ✅ Allowed

Back-to-back appointments are allowed:

10:00 - 11:00   Patient A
11:00 - 12:00   Patient B

The backend performs the conflict check before creating an appointment.

2. Appointment Rescheduling

An existing appointment can be moved to a new date and time.

When rescheduling, ClinicFlow:

Finds the appointment.
Verifies the logged-in patient owns it.
Checks that the appointment is still booked.
Validates the new time.
Checks for doctor schedule conflicts.
Rejects overlapping slots.
Keeps the same patient and doctor.

Example:

Old:
10:00 - 11:00

New:
14:00 - 15:00

If the new slot is already occupied:

14:00 - 15:00   Patient B

Patient A → 14:30 - 15:30

Result: ❌ Conflict
3. Fair Cancellation Policy

ClinicFlow uses a simple cancellation rule.

Cancellation Time	Fee
24 hours or more before appointment	₹0
Less than 24 hours before appointment	₹200
Early Cancellation
Appointment:
20 September, 10:00 AM

Cancelled:
18 September, 10:00 AM

Fee:
₹0
Late Cancellation
Appointment:
20 September, 10:00 AM

Cancelled:
19 September, 12:00 PM

Fee:
₹200

The backend calculates the fee automatically.

4. Patient Appointment Search

The front desk can search appointments using the patient's name.

Example:

Search: Brijesh

Brijesh Singh
Dr. Sharma
20 September 2026
10:00 - 11:00
Booked

Partial name matching is supported.

5. Doctor Daily Schedule

The front desk can select a doctor and date to view the doctor's appointments.

Example:

Dr. Sharma — 20 September 2026

10:00 - 11:00    Brijesh Singh
11:00 - 12:00    Rahul Kumar
12:00 - 01:00    Priya Sharma

Appointments are returned in time order.

6. Daily Appointment Reminders

ClinicFlow includes a notification outbox for appointment reminders.

The automation can be triggered using:

POST /clock

For today's booked appointments, reminder notifications are created.

Example:

Reminder:
You have an appointment with Dr. Sharma today at 10:00.

Notifications can be viewed using:

GET /outbox

The notification outbox provides an integration point for a future SMS, email, or WhatsApp Notification Service.

7. Automatic No-Show Detection

ClinicFlow automatically detects appointments that were not completed.

If an appointment remains booked for 30 minutes after its start time, it is automatically marked as:

no_show

Example:

Appointment:
10:00 AM

Clock:
10:30 AM

Status:
no_show

Before 30 minutes:

10:29 AM → booked

At 30 minutes:

10:30 AM → no_show

Completed or cancelled appointments are not marked as no-show.

8. Appointment Completion

A booked appointment can be marked as completed.

booked → completed

Completed appointments are excluded from the no-show automation.

9. Pagination and Sorting

The appointment listing API supports:

Pagination
Page size
Sorting
Ascending order
Descending order

Example:

GET /appointments?page=1&page_size=10&sort_by=appointment_date&sort_order=asc
🎯 Target Users

ClinicFlow is designed for:

Clinic receptionists
Front-desk staff
Small clinics
Multi-doctor clinics
Appointment coordinators
Patients
🔄 How ClinicFlow Works
                    ┌─────────────────┐
                    │     Patient     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  ClinicFlow UI  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    REST APIs    │
                    │     FastAPI     │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        ┌──────────┐   ┌──────────┐   ┌─────────────┐
        │  Users   │   │ Doctors  │   │ Appointments│
        └──────────┘   └──────────┘   └─────────────┘
                                              │
                                              ▼
                                     ┌─────────────────┐
                                     │     SQLite      │
                                     │    Database     │
                                     └─────────────────┘
🛠️ Tech Stack
Frontend
HTML5
CSS3
JavaScript
Fetch API
Responsive CSS
Backend
Python
FastAPI
Pydantic
Uvicorn
Database
SQLite
SQLAlchemy ORM
Authentication
Token-based authentication
Password hashing
Development Tools
Git
GitHub
VS Code
Swagger / OpenAPI
📁 Project Structure
clinic_appointments/
│
├── main.py
├── requirements.txt
│
├── README.md
├── REASONING.md
├── AI_LOGS.md
│
├── static/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
└── clinicflow.db

clinicflow.db is the local SQLite database generated by the application.
__pycache__/ and Python cache files should not be committed.

⚙️ Installation
1. Clone the Repository
git clone https://github.com/brijesh4704/clinic_appointments.git
cd clinic_appointments
2. Create a Virtual Environment
Windows
python -m venv venv
venv\Scripts\activate
macOS / Linux
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
▶️ Run the Application

Start the FastAPI server:

uvicorn main:app --reload --host 0.0.0.0 --port 8000

Open:

http://localhost:8000

The ClinicFlow UI will be available directly from the FastAPI application.

📚 API Documentation

FastAPI automatically provides interactive API documentation.

Swagger UI
http://localhost:8000/docs
ReDoc
http://localhost:8000/redoc

Swagger can be used to test all REST APIs directly from the browser.

🔐 Authentication APIs
Register
POST /auth/register

Creates a new user account.

Example:

{
  "name": "Brijesh Singh",
  "email": "brijesh@example.com",
  "password": "password123"
}
Login
POST /auth/login

Authenticates the user and returns an access token.

The token is used for protected appointment operations.

👨‍⚕️ Doctor APIs
Get Doctors
GET /doctors

Returns the available doctors.

Create Doctor
POST /doctors

Example:

{
  "name": "Dr. Sharma",
  "specialization": "General Physician"
}
📅 Appointment APIs
Create Appointment
POST /appointments

Creates an appointment after checking for doctor conflicts.

Get Appointments
GET /appointments

Supports pagination and sorting.

Example:

GET /appointments?page=1&page_size=10&sort_by=appointment_date&sort_order=asc
Get Appointment
GET /appointments/{appointment_id}

Returns a single appointment.

Search Patient Appointments
GET /appointments/search?patientName=Brijesh

Searches appointments using the patient's name.

Doctor Daily Schedule
GET /doctors/{doctor_id}/appointments?appointment_date=2026-09-20

Returns appointments for a doctor on a selected date.

Cancel Appointment
PATCH /appointments/{appointment_id}/cancel

Cancels an appointment and calculates the applicable cancellation fee.

Reschedule Appointment
PATCH /appointments/{appointment_id}/reschedule

Example:

{
  "appointment_date": "2026-09-20",
  "start_time": "14:00",
  "end_time": "15:00"
}

The new slot is checked for conflicts before the appointment is updated.

Complete Appointment
PATCH /appointments/{appointment_id}/complete

Marks a booked appointment as completed.

🔔 Notification APIs
Run Clock Automation
POST /clock

Runs the time-based appointment automation.

It performs:

Today's appointment reminder creation.
No-show detection.

Optional request:

{
  "now": "2026-09-20T10:30:00"
}

The optional now value allows deterministic testing of time-based behavior.

View Notification Outbox
GET /outbox

Returns generated appointment reminder notifications.

Example:

{
  "appointment_id": 1,
  "patient_id": 2,
  "message": "Reminder: You have an appointment with Dr. Sharma today at 10:00."
}
🧪 Testing the Core Rules
Test 1 — Normal Booking

Create:

10:00 - 11:00

Expected:

200 OK
Test 2 — Overlapping Booking

Existing:

10:00 - 11:00

New:

10:30 - 11:30

Expected:

409 Conflict
Test 3 — Back-to-Back Booking

Existing:

10:00 - 11:00

New:

11:00 - 12:00

Expected:

200 OK

Back-to-back appointments are allowed.

Test 4 — Reschedule Conflict

Existing appointments:

Patient A: 10:00 - 11:00
Patient B: 14:00 - 15:00

Try:

Patient A → 14:30 - 15:30

Expected:

409 Conflict
Test 5 — Valid Reschedule

Try:

Patient A → 12:00 - 13:00

Expected:

200 OK

The doctor and patient remain unchanged.

Test 6 — Early Cancellation

Cancel 24 hours or more before the appointment.

Expected:

Fee = ₹0
Test 7 — Late Cancellation

Cancel less than 24 hours before the appointment.

Expected:

Fee = ₹200
Test 8 — Daily Reminder

Run:

POST /clock

for a day containing booked appointments.

Expected:

reminders_created >= 1

Then:

GET /outbox

The reminder should be present.

Test 9 — No-Show

Suppose an appointment starts at:

10:00 AM

Run:

POST /clock

with:

{
  "now": "2026-09-20T10:30:00"
}

Expected:

status = no_show

At 10:29:

booked

At 10:30:

no_show
🗄️ Database Schema

ClinicFlow uses SQLite with SQLAlchemy ORM.

User

Stores:

User ID
Name
Email
Password information
Doctor

Stores:

Doctor ID
Doctor name
Specialization
Appointment

Stores:

Appointment ID
Doctor ID
Patient ID
Appointment date
Start time
End time
Status
Cancellation fee
Creation time
NotificationOutbox

Stores:

Notification ID
Appointment ID
Patient ID
Reminder message
Creation time
Sent status
🔒 Business Rules
Rule 1 — No Doctor Overlap

Two booked appointments for the same doctor cannot overlap.

The overlap condition is:

existing.start < new.end
AND
existing.end > new.start
Rule 2 — Back-to-Back Appointments Are Allowed
Existing: 10:00 - 11:00
New:      11:00 - 12:00

This is valid.

Rule 3 — Rescheduling Must Be Conflict-Free

Every reschedule request performs the same overlap validation as a new booking.

Rule 4 — Cancellation Fee
>= 24 hours → ₹0
< 24 hours  → ₹200
Rule 5 — No-Show

A booked appointment becomes:

no_show

30 minutes after its start time if it has not been completed or cancelled.

Rule 6 — Completed Appointments

Completed appointments are not converted into no-show.

Rule 7 — Reminder Deduplication

ClinicFlow creates at most one reminder notification for each appointment in the notification outbox.

🧭 Application Workflow
Open ClinicFlow
      │
      ▼
Register / Login
      │
      ▼
Dashboard
      │
      ├── Book Appointment
      │       │
      │       ▼
      │   Conflict Check
      │
      ├── Search Patient
      │
      ├── Doctor Schedule
      │
      ├── Reschedule
      │       │
      │       ▼
      │   Conflict Check
      │
      ├── Cancel
      │       │
      │       ▼
      │   Calculate Fee
      │
      └── Complete Appointment
🧠 Design Decisions

The most important requirement is:

A doctor must never be double-booked.

Therefore, appointment conflict validation is implemented in the backend rather than relying only on the frontend.

The frontend provides the user experience, while the backend enforces the actual business rules.

The rescheduling operation reuses the same conflict detection logic used for new bookings.

The notification outbox provides a simple integration boundary for a future external Notification Service.

The /clock endpoint allows time-based automation to be triggered deterministically during testing.

🐛 Debugging

Check Python syntax:

python -m py_compile main.py

Start the server:

uvicorn main:app --reload --host 0.0.0.0 --port 8000

Then open:

http://localhost:8000/docs

If the local database needs to be reset during development:

Stop the server.
Remove clinicflow.db.
Start the server again.

The database tables will be created automatically.

📦 Requirements

Install dependencies using:

pip install -r requirements.txt

The project requires Python 3 or later and the packages listed in requirements.txt.

🚀 Demo Data

For quick testing, ClinicFlow provides:

POST /demo/seed

This endpoint can be used to create demonstration doctors and appointment data.

🔮 Future Features
1. SMS / WhatsApp Reminders

Connect the notification outbox to an external notification provider.

2. Online Payments

Allow patients to pay consultation charges and cancellation fees online.

3. Doctor Availability

Allow doctors to configure:

Working hours
Breaks
Holidays
Leave
Available appointment slots
📄 Assessment Documentation
REASONING.md

Contains:

Problem understanding
Architecture decisions
Business rules
Testing approach
Bugs encountered
Fixes implemented
AI_LOGS.md

Contains the complete AI conversation used during development as required by the assessment.

📌 Project Status
✅ User Registration
✅ User Login
✅ Doctor Management
✅ Appointment Booking
✅ Conflict Detection
✅ Back-to-Back Appointments
✅ Patient Appointment Search
✅ Doctor Daily Schedule
✅ Cancellation Fee
✅ Appointment Rescheduling
✅ Appointment Completion
✅ Daily Reminder Outbox
✅ Automatic No-Show Detection
✅ Pagination
✅ Sorting
✅ Responsive UI
✅ REST APIs
✅ SQLite Database
✅ Swagger Documentation
👨‍💻 Author

Brijesh Singh

B.Tech — Computer Science & Data Science

Swami Keshvanand Institute of Technology, Management & Gramothan (SKIT), Jaipur

⭐ ClinicFlow

Appointments that stay conflict-free.

Built to help clinic front desks manage appointments without double-booking doctors.


After pasting:

```bash
git add README.md
git commit -m "Add complete project README"
git push origin main

Then your GitHub repository will have a much more professional README for the assessment.

Pasted markdown(4).md
File

Yes. I reviewed the uploaded Prescripto README. Its structure is useful for your project—hero → features → screenshots/UI → tech stack → structure → setup → API → roadmap → author—but you should not copy Prescripto's React/Node/MongoDB claims, because your ClinicFlow implementation is FastAPI + SQLite + HTML/CSS/JS.

For your Auriga assessment, use the ClinicFlow README I gave above, but I recommend adding a Screenshots/UI section modeled on the uploaded README's presentation style. The source README uses a dedicated screenshots section with separate UI areas.

Add this section after # 🖥️ User Interface
# 📸 Screenshots

## 🏠 Landing Page

The ClinicFlow landing page introduces the product, its core features, target users, and the appointment workflow.

![ClinicFlow Landing Page](screenshots/landing-page.png)

---

## 🔐 Login & Registration

Users can create an account and securely log in before managing appointments.

![ClinicFlow Login](screenshots/login.png)

![ClinicFlow Registration](screenshots/register.png)

---

## 📊 Appointment Dashboard

The dashboard provides a centralized view of appointments with options to book, search, reschedule, cancel, and complete appointments.

![ClinicFlow Dashboard](screenshots/dashboard.png)

---

## 📅 Book Appointment

Users can select a doctor, date, start time, and end time.

The backend validates the requested slot before creating the appointment.

![Book Appointment](screenshots/book-appointment.png)

---

## 👨‍⚕️ Doctor Daily Schedule

The schedule view allows the front desk to see all appointments for a doctor on a selected date.

![Doctor Schedule](screenshots/doctor-schedule.png)

---

## 🔎 Patient Search

The front desk can search for appointments using a patient's name.

![Patient Search](screenshots/patient-search.png)

---

## 🔄 Reschedule Appointment

Appointments can be moved to a new time while preserving the same doctor and patient.

The new slot is checked again for conflicts.

![Reschedule Appointment](screenshots/reschedule.png)

---

## ❌ Cancellation

The system automatically calculates the cancellation fee based on the cancellation time.

![Cancel Appointment](screenshots/cancellation.png)

---

## 🔔 Notification Outbox

The notification outbox displays reminders generated for today's appointments.

![Notification Outbox](screenshots/notifications.png)

---

## 🚫 No-Show Automation

Appointments that remain incomplete for 30 minutes after their start time are automatically marked as `no_show`.

![No Show](screenshots/no-show.png)

---

## 📖 API Documentation

ClinicFlow provides interactive API documentation through FastAPI Swagger UI.

![Swagger API Documentation](screenshots/swagger.png)
Your GitHub structure should then look like
clinic_appointments/
│
├── main.py
├── requirements.txt
├── clinicflow.db
│
├── README.md
├── REASONING.md
├── AI_LOGS.md
│
├── static/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
└── screenshots/
    ├── landing-page.png
    ├── login.png
    ├── register.png
    ├── dashboard.png
    ├── book-appointment.png
    ├── doctor-schedule.png
    ├── patient-search.png
    ├── reschedule.png
    ├── cancellation.png
    ├── notifications.png
    ├── no-show.png
    └── swagger.png

Don't add screenshot filenames until you actually have those screenshots. GitHub will show broken images if the files don't exist.

For the assessment, this will make the README look much more like a real product/project README while remaining truthful to your actual ClinicFlow implementation.