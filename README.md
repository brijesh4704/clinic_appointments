# ClinicFlow

Appointment scheduling for a small clinic. A doctor can never be double-booked, and a
cancellation made inside the notice window carries a fee that the system works out for you.

Built for the Auriga IT Round 2 builder round.

- Backend: FastAPI (Python)
- Database: SQLite via SQLAlchemy ORM
- Frontend: plain HTML, CSS and JavaScript, served by the same app
- Auth: email + password, PBKDF2 hashing, HS256 bearer tokens

---

## Setup

Requires Python 3.9 or newer.

```bash
git clone <your-repo-url>
cd clinicflow

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

## Run

```bash
python -m app.seed                 # optional: demo doctors, patients and appointments
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Then open:

| URL | What it is |
| --- | --- |
| `/` | Landing page |
| `/app` | The front-desk application |
| `/docs` | Interactive API reference (Swagger UI) |

In GitHub Codespaces, open the forwarded port 8000 from the **Ports** tab. Set the port's
visibility to **Public** if you want to share the link.

### Demo accounts (after seeding)

| Role | Email | Password |
| --- | --- | --- |
| Front-desk staff | `desk@clinicflow.test` | `desk1234` |
| Patient | `rahul@example.com` | `patient123` |

Staff see and manage every appointment. Patients see and cancel only their own.

## Configuration

Every rule is an environment variable, so a clinic can match its own policy without
touching code.

| Variable | Default | What it controls |
| --- | --- | --- |
| `DATABASE_URL` | `sqlite:///./clinic.db` | Database connection |
| `SECRET_KEY` | `dev-secret-change-me-in-production` | Token signing key |
| `TOKEN_TTL_SECONDS` | `43200` | How long a sign-in lasts |
| `LATE_CANCEL_WINDOW_HOURS` | `24` | Notice needed for a free cancellation |
| `LATE_CANCEL_FEE` | `200` | Fee charged for a late cancellation |
| `MAX_APPOINTMENT_MINUTES` | `240` | Longest bookable slot |

## Tests

```bash
python -m tests.test_api
```

39 checks covering booking conflicts, back-to-back slots, the fee rule, access control,
search, sorting and pagination. Exits non-zero if anything fails.

## Debugging

| Symptom | Fix |
| --- | --- |
| `ModuleNotFoundError: app` | Run `uvicorn` from the repository root, not from `app/` |
| `401 Sign in to continue` | The bearer token is missing or expired — sign in again |
| Port 8000 already in use | `uvicorn main:app --port 8001`, or `lsof -ti:8000 \| xargs kill` |
| Schema looks stale after a model change | `rm clinic.db && python -m app.seed` |
| Frontend shows nothing | Open the browser console; the API error text is surfaced there and in the on-page banner |
| Codespaces link 404s | Open the port from the **Ports** tab rather than typing `localhost` |

`--reload` restarts the server on every save, and uvicorn prints the full traceback for any
unhandled error. Every API error also returns a readable `detail` string, which the UI shows
as-is.

---

## API endpoints

All `/api` routes except `register`, `login` and `health` need
`Authorization: Bearer <token>`.

### Auth

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/api/auth/register` | Create an account (`PATIENT` or `STAFF`) and return a token |
| `POST` | `/api/auth/login` | Exchange email and password for a token |
| `GET` | `/api/auth/me` | The signed-in account |

### Doctors

| Method | Path | What it does |
| --- | --- | --- |
| `GET` | `/api/doctors` | Search + paginate the roster. Query: `q`, `page`, `page_size`, `sort_by` (`name`, `specialization`, `consultation_fee`, `created_at`), `order` |
| `POST` | `/api/doctors` | Add a doctor (staff only) |
| `GET` | `/api/doctors/{id}` | One doctor |
| `GET` | `/api/doctors/{id}/schedule?date=YYYY-MM-DD` | That doctor's day in clock order. Optional `include_cancelled` |

### Appointments

| Method | Path | What it does |
| --- | --- | --- |
| `POST` | `/api/appointments` | Book a slot. `409` if it overlaps a live appointment for the same doctor |
| `GET` | `/api/appointments` | Search, filter, sort, paginate. Query: `q`, `doctor_id`, `status`, `date_from`, `date_to`, `mine`, `page`, `page_size`, `sort_by` (`start_time`, `created_at`, `patient_name`, `status`, `cancellation_fee`), `order` |
| `GET` | `/api/appointments/{id}` | One appointment |
| `GET` | `/api/appointments/{id}/cancellation-preview` | What cancelling right now would cost, before committing |
| `DELETE` | `/api/appointments/{id}` | Cancel, applying the late fee if inside the window |

### Patients

| Method | Path | What it does |
| --- | --- | --- |
| `GET` | `/api/patients` | Search the patient directory (staff only). Query: `q`, `page`, `page_size`, `sort_by`, `order` |

### Meta

| Method | Path | What it does |
| --- | --- | --- |
| `GET` | `/api/health` | Liveness plus the active cancellation policy |

### Example

```bash
BASE=http://localhost:8000

TOKEN=$(curl -s -X POST $BASE/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"desk@clinicflow.test","password":"desk1234"}' | python -c "import sys,json;print(json.load(sys.stdin)['access_token'])")

curl -s -X POST $BASE/api/appointments \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"doctor_id":1,"start_time":"2026-09-20T10:00:00","end_time":"2026-09-20T10:30:00","reason":"Follow-up"}'

# The same slot again -> 409 with the clashing appointment named
# 10:30-11:00 -> 201, because back-to-back is not an overlap
```

---

## Mandatory requirements, and where they live

| Requirement | Where |
| --- | --- |
| Database with a sensible schema | `app/models.py` — users, doctors, appointments with foreign keys and indexes |
| REST APIs for core operations | `app/routers/`, listed above |
| A usable UI over those APIs | `static/app.html`, `static/app.js` |
| Registration and login | `app/routers/auth_router.py`, `app/auth.py` |
| Search | Appointments, doctors and patients all accept `q` |
| Landing page | `static/index.html` |
| Pagination and sorting | `app/services.py::paginate`, used by every list endpoint |

## Project layout

```
clinicflow/
├── main.py                  # app wiring, static routes, health
├── app/
│   ├── database.py          # engine, session, Base
│   ├── models.py            # User, Doctor, Appointment
│   ├── schemas.py           # request/response models
│   ├── auth.py              # PBKDF2 hashing + HS256 tokens (stdlib only)
│   ├── services.py          # overlap rule, fee rule, pagination
│   ├── seed.py              # demo data
│   └── routers/             # auth, doctors, appointments, patients
├── static/                  # landing page, app shell, CSS, JS
├── tests/test_api.py        # 39 end-to-end checks
├── requirements.txt
├── REASONING.md
└── AI_LOGS.md
```
