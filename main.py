from datetime import datetime, date, time, timedelta
from typing import Optional
import hashlib
import secrets

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Date,
    Time,
    DateTime,
    ForeignKey,
    Float,
    Boolean,
)
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship


# ============================================================
# DATABASE
# ============================================================

DATABASE_URL = "sqlite:///./clinicflow.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String(300), nullable=False)

    appointments = relationship("Appointment", back_populates="patient")


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    specialization = Column(String(100), nullable=False)

    appointments = relationship("Appointment", back_populates="doctor")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    appointment_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    status = Column(String(30), default="booked")
    cancellation_fee = Column(Float, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)

    doctor = relationship("Doctor", back_populates="appointments")
    patient = relationship("User", back_populates="appointments")


# ============================================================
# NOTIFICATION OUTBOX
# ============================================================

class NotificationOutbox(Base):
    __tablename__ = "notification_outbox"

    id = Column(Integer, primary_key=True, index=True)

    appointment_id = Column(
        Integer,
        ForeignKey("appointments.id"),
        nullable=False
    )

    patient_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    message = Column(String(500), nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    sent = Column(Boolean, default=False)


Base.metadata.create_all(bind=engine)


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="ClinicFlow API",
    description="Clinic front-desk appointment management system",
    version="1.0.0",
)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# AUTH HELPERS
# ============================================================

security = HTTPBearer()

tokens = {}


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        100000
    ).hex()

    return f"{salt}${password_hash}"


def verify_password(password: str, stored: str) -> bool:
    try:
        salt, stored_hash = stored.split("$")

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            salt.encode(),
            100000
        ).hex()

        return secrets.compare_digest(password_hash, stored_hash)

    except ValueError:
        return False


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    user_id = tokens.get(token)

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user


# ============================================================
# SCHEMAS
# ============================================================

class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: str
    password: str = Field(min_length=6)


class LoginRequest(BaseModel):
    email: str
    password: str


class DoctorRequest(BaseModel):
    name: str
    specialization: str


class AppointmentRequest(BaseModel):
    doctor_id: int
    appointment_date: date
    start_time: time
    end_time: time


class RescheduleRequest(BaseModel):
    appointment_date: date
    start_time: time
    end_time: time


class ClockRequest(BaseModel):
    now: Optional[datetime] = None


# ============================================================
# LANDING PAGE
# ============================================================

@app.get("/")
def landing_page():
    return FileResponse("static/index.html")


# ============================================================
# AUTH
# ============================================================

@app.post("/auth/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    existing = db.query(User).filter(
        User.email == request.email.lower()
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user = User(
        name=request.name,
        email=request.email.lower(),
        password_hash=hash_password(request.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "Registration successful",
        "user_id": user.id
    }


@app.post("/auth/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == request.email.lower()
    ).first()

    if not user or not verify_password(
        request.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = secrets.token_urlsafe(32)
    tokens[token] = user.id

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }


# ============================================================
# DOCTORS
# ============================================================

@app.get("/dashboard")
def dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    today = date.today()
    return {
        "total_doctors": db.query(Doctor).count(),
        "total_patients": db.query(User).count(),
        "today_appointments": db.query(Appointment).filter(Appointment.appointment_date == today).count(),
        "no_shows": db.query(Appointment).filter(Appointment.status == "no_show").count(),
        "cancelled": db.query(Appointment).filter(Appointment.status == "cancelled").count(),
        "completed": db.query(Appointment).filter(Appointment.status == "completed").count(),
    }


@app.get("/doctors")
def get_doctors(
    db: Session = Depends(get_db)
):
    doctors = db.query(Doctor).order_by(Doctor.name.asc()).all()

    return [
        {
            "id": doctor.id,
            "name": doctor.name,
            "specialization": doctor.specialization
        }
        for doctor in doctors
    ]


@app.post("/doctors")
def create_doctor(
    request: DoctorRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    doctor = Doctor(
        name=request.name,
        specialization=request.specialization
    )

    db.add(doctor)
    db.commit()
    db.refresh(doctor)

    return {
        "message": "Doctor created",
        "doctor": {
            "id": doctor.id,
            "name": doctor.name,
            "specialization": doctor.specialization
        }
    }


# ============================================================
# APPOINTMENT CONFLICT CHECK
# ============================================================

def has_overlap(
    db: Session,
    doctor_id: int,
    appointment_date: date,
    start_time: time,
    end_time: time,
    exclude_id: Optional[int] = None
):

    query = db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        Appointment.appointment_date == appointment_date,
        Appointment.status == "booked",
        Appointment.start_time < end_time,
        Appointment.end_time > start_time,
    )

    if exclude_id:
        query = query.filter(Appointment.id != exclude_id)

    return query.first()


# ============================================================
# CREATE APPOINTMENT
# ============================================================

@app.post("/appointments")
def create_appointment(
    request: AppointmentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if request.start_time >= request.end_time:
        raise HTTPException(
            status_code=400,
            detail="End time must be after start time"
        )

    doctor = db.query(Doctor).filter(
        Doctor.id == request.doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    conflict = has_overlap(
        db,
        request.doctor_id,
        request.appointment_date,
        request.start_time,
        request.end_time
    )

    if conflict:
        raise HTTPException(
            status_code=409,
            detail="Doctor is already booked during this time"
        )

    appointment = Appointment(
        doctor_id=request.doctor_id,
        patient_id=current_user.id,
        appointment_date=request.appointment_date,
        start_time=request.start_time,
        end_time=request.end_time,
        status="booked",
        cancellation_fee=0
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return appointment_response(appointment)


# ============================================================
# APPOINTMENT RESPONSE
# ============================================================

def appointment_response(appointment: Appointment):

    return {
        "id": appointment.id,
        "doctor_id": appointment.doctor_id,
        "doctor_name": appointment.doctor.name,
        "patient_id": appointment.patient_id,
        "patient_name": appointment.patient.name,
        "patient_email": appointment.patient.email,
        "appointment_date": appointment.appointment_date.isoformat(),
        "start_time": appointment.start_time.strftime("%H:%M"),
        "end_time": appointment.end_time.strftime("%H:%M"),
        "status": appointment.status,
        "cancellation_fee": appointment.cancellation_fee
    }


# ============================================================
# LIST APPOINTMENTS
# ============================================================

@app.get("/appointments")
def get_appointments(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    sort_by: str = Query("appointment_date"),
    order: str = Query("asc"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    allowed_sorting = {
        "appointment_date": Appointment.appointment_date,
        "start_time": Appointment.start_time,
        "status": Appointment.status,
        "id": Appointment.id
    }

    sort_column = allowed_sorting.get(
        sort_by,
        Appointment.appointment_date
    )

    if order.lower() == "desc":
        sort_column = sort_column.desc()
    else:
        sort_column = sort_column.asc()

    query = db.query(Appointment).order_by(sort_column)

    total = query.count()

    appointments = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "items": [
            appointment_response(a)
            for a in appointments
        ],
        "page": page,
        "limit": limit,
        "total": total,
        "pages": (total + limit - 1) // limit
    }


# ============================================================
# GET APPOINTMENT
# ============================================================

@app.get("/appointments/{appointment_id}")
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    return appointment_response(appointment)


# ============================================================
# SEARCH BY PATIENT NAME
# ============================================================

@app.get("/appointments/search")
def search_appointments(
    patientName: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    query = db.query(Appointment).join(User).filter(
        User.name.ilike(f"%{patientName}%")
    ).order_by(
        Appointment.appointment_date.asc(),
        Appointment.start_time.asc()
    )

    total = query.count()

    appointments = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "items": [
            appointment_response(a)
            for a in appointments
        ],
        "page": page,
        "limit": limit,
        "total": total
    }


# ============================================================
# DOCTOR'S DAY
# ============================================================

@app.get("/doctors/{doctor_id}/appointments")
def doctor_schedule(
    doctor_id: int,
    appointment_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    appointments = db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        Appointment.appointment_date == appointment_date
    ).order_by(
        Appointment.start_time.asc()
    ).all()

    return {
        "doctor": {
            "id": doctor.id,
            "name": doctor.name,
            "specialization": doctor.specialization
        },
        "date": appointment_date.isoformat(),
        "appointments": [
            appointment_response(a)
            for a in appointments
        ]
    }


# ============================================================
# CANCEL APPOINTMENT
# ============================================================

@app.patch("/appointments/{appointment_id}/cancel")
def cancel_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    if appointment.status == "cancelled":
        raise HTTPException(
            status_code=400,
            detail="Appointment is already cancelled"
        )

    appointment_datetime = datetime.combine(
        appointment.appointment_date,
        appointment.start_time
    )

    now = datetime.now()

    hours_remaining = (
        appointment_datetime - now
    ).total_seconds() / 3600

    # Assumption:
    # 24 hours or more = free cancellation
    # Less than 24 hours = ₹200 fee

    if hours_remaining >= 24:
        fee = 0
    else:
        fee = 200

    appointment.status = "cancelled"
    appointment.cancellation_fee = fee

    db.commit()
    db.refresh(appointment)

    return {
        "message": "Appointment cancelled",
        "appointment_id": appointment.id,
        "cancellation_fee": fee,
        "policy": (
            "Free if cancelled 24 or more hours before "
            "the appointment; otherwise ₹200."
        )
    }



# ============================================================
# COMPLETE APPOINTMENT
# ============================================================

@app.patch("/appointments/{appointment_id}/complete")
def complete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    if appointment.patient_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only complete your own appointment"
        )

    if appointment.status != "booked":
        raise HTTPException(
            status_code=400,
            detail="Only booked appointments can be completed"
        )

    appointment.status = "completed"
    db.commit()
    db.refresh(appointment)

    return {
        "message": "Appointment completed",
        "appointment": appointment_response(appointment)
    }

# ============================================================
# RESCHEDULE APPOINTMENT
# ============================================================

@app.patch("/appointments/{appointment_id}/reschedule")
def reschedule_appointment(
    appointment_id: int,
    request: RescheduleRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    if appointment.patient_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only reschedule your own appointment"
        )

    if appointment.status != "booked":
        raise HTTPException(
            status_code=400,
            detail="Only booked appointments can be rescheduled"
        )

    if request.start_time >= request.end_time:
        raise HTTPException(
            status_code=400,
            detail="End time must be after start time"
        )

    # Re-check the same doctor's schedule, excluding this appointment.
    conflict = has_overlap(
        db,
        appointment.doctor_id,
        request.appointment_date,
        request.start_time,
        request.end_time,
        exclude_id=appointment.id
    )

    if conflict:
        raise HTTPException(
            status_code=409,
            detail="Doctor is already booked during this time"
        )

    # Patient and doctor remain unchanged.
    appointment.appointment_date = request.appointment_date
    appointment.start_time = request.start_time
    appointment.end_time = request.end_time

    db.commit()
    db.refresh(appointment)

    return {
        "message": "Appointment rescheduled successfully",
        "appointment": appointment_response(appointment)
    }


# ============================================================
# CLOCK / AUTOMATION
# ============================================================

@app.post("/clock")
def run_clock(
    request: ClockRequest = ClockRequest(),
    db: Session = Depends(get_db)
):
    """
    Trigger scheduled clinic jobs.

    T1: Create one reminder notification for each booked
        appointment scheduled on the current clock date.

    T2: Mark booked appointments as no-show once their start
        time is at least 30 minutes in the past.

    The optional `now` field makes the endpoint deterministic
    for automated grading and local testing.
    """
    now = request.now or datetime.now()
    today = now.date()

    # --------------------------------------------------------
    # T1: Morning reminders for today's appointments
    # --------------------------------------------------------

    todays_appointments = db.query(Appointment).filter(
        Appointment.appointment_date == today,
        Appointment.status == "booked"
    ).order_by(
        Appointment.start_time.asc()
    ).all()

    reminders_created = 0

    for appointment in todays_appointments:
        existing_notification = db.query(
            NotificationOutbox
        ).filter(
            NotificationOutbox.appointment_id == appointment.id
        ).first()

        if existing_notification:
            continue

        message = (
            f"Reminder: You have an appointment with "
            f"{appointment.doctor.name} today at "
            f"{appointment.start_time.strftime('%H:%M')}."
        )

        notification = NotificationOutbox(
            appointment_id=appointment.id,
            patient_id=appointment.patient_id,
            message=message,
            sent=False
        )

        db.add(notification)
        reminders_created += 1

    # --------------------------------------------------------
    # T2: Automatic no-show after 30 minutes
    # --------------------------------------------------------

    booked_appointments = db.query(Appointment).filter(
        Appointment.status == "booked"
    ).all()

    no_shows_marked = 0

    for appointment in booked_appointments:
        appointment_start = datetime.combine(
            appointment.appointment_date,
            appointment.start_time
        )

        minutes_after_start = (
            now - appointment_start
        ).total_seconds() / 60

        if minutes_after_start >= 30:
            appointment.status = "no_show"
            no_shows_marked += 1

    db.commit()

    return {
        "message": "Clock processed successfully",
        "clock_time": now.isoformat(),
        "date": today.isoformat(),
        "reminders_created": reminders_created,
        "no_shows_marked": no_shows_marked
    }


# ============================================================
# NOTIFICATION OUTBOX
# ============================================================

@app.get("/outbox")
def get_outbox(
    db: Session = Depends(get_db)
):
    """
    Notification Service outbox used by the assessment
    integration test after POST /clock.
    """
    notifications = db.query(
        NotificationOutbox
    ).order_by(
        NotificationOutbox.created_at.desc()
    ).all()

    return {
        "items": [
            {
                "id": notification.id,
                "appointment_id": notification.appointment_id,
                "patient_id": notification.patient_id,
                "message": notification.message,
                "created_at": notification.created_at.isoformat(),
                "sent": notification.sent
            }
            for notification in notifications
        ],
        "total": len(notifications)
    }


# ============================================================
# DEMO DATA
# ============================================================

@app.post("/demo/seed")
def seed_demo_data(
    db: Session = Depends(get_db)
):

    if db.query(Doctor).count() == 0:

        doctors = [
            Doctor(
                name="Dr. Sharma",
                specialization="General Physician"
            ),
            Doctor(
                name="Dr. Mehta",
                specialization="Dermatologist"
            ),
            Doctor(
                name="Dr. Kapoor",
                specialization="Cardiologist"
            )
        ]

        db.add_all(doctors)
        db.commit()

    return {
        "message": "Demo doctors are ready",
        "doctors": [
            {
                "id": d.id,
                "name": d.name,
                "specialization": d.specialization
            }
            for d in db.query(Doctor).all()
        ]
    }
