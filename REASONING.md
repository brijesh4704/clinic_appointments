# ClinicFlow — Reasoning

## 1. Problem Understanding

The problem describes a busy clinic where the front desk manages appointments for multiple doctors.

The main problems identified were:

1. A doctor can accidentally be double-booked.
2. Two patients may try to book the same or overlapping time slot.
3. Patients may cancel appointments.
4. Early cancellations should be free.
5. Late cancellations should have a small fee.
6. The front desk needs to view a doctor's appointments for a particular day.
7. The front desk needs to search for a patient's appointments by name.

The solution was designed as a general appointment management system that can work for a small clinic.

The main priority was to make appointment booking conflict-free before implementing secondary lookup features.

---

## 2. Solution Approach

The application is called **ClinicFlow**.

It is a full-stack web application with:

- FastAPI backend
- SQLite database
- SQLAlchemy ORM
- HTML/CSS/JavaScript frontend
- REST APIs
- Token-based authentication
- Appointment conflict detection
- Patient search
- Doctor daily schedule
- Pagination
- Sorting
- Cancellation handling

The architecture was kept relatively simple because the assessment has a strict time limit.

### High-Level Architecture

```text
User
  |
  v
HTML / CSS / JavaScript UI
  |
  v
FastAPI REST API
  |
  v
SQLAlchemy ORM
  |
  v
SQLite Database