from sqlalchemy.orm import Session
from sqlalchemy import and_

from datetime import datetime
from datetime import date
from datetime import time

from models import User
from models import Appointment
from models import ConversationSession


AVAILABLE_SLOTS = [

    "09:00",

    "10:00",

    "11:00",

    "14:00",

    "15:00",

    "16:00"

]


def identify_user(
    db: Session,
    phone_number: str,
    name: str = None
):

    user = db.query(User).filter(
        User.phone_number == phone_number
    ).first()

    if user:

        if name:

            user.name = name

            db.commit()

            db.refresh(user)

        return {

            "success": True,

            "user_id": user.id,

            "name": user.name,

            "phone_number": user.phone_number,

            "message": "User found"

        }

    new_user = User(

        phone_number=phone_number,

        name=name

    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {

        "success": True,

        "user_id": new_user.id,

        "name": new_user.name,

        "phone_number": new_user.phone_number,

        "message": "New user created"

    }


def fetch_slots(
    db: Session,
    booking_date: str
):

    booking_date = datetime.strptime(
        booking_date,
        "%Y-%m-%d"
    ).date()

    booked = db.query(
        Appointment
    ).filter(

        Appointment.date == booking_date,

        Appointment.status == "booked"

    ).all()

    booked_times = [

        a.time.strftime("%H:%M")

        for a in booked

    ]

    available = [

        slot

        for slot in AVAILABLE_SLOTS

        if slot not in booked_times

    ]

    return {

        "success": True,

        "date": str(booking_date),

        "available_slots": available

    }


def book_appointment(

    db: Session,

    user_id: int,

    booking_date: str,

    booking_time: str

):

    booking_date = datetime.strptime(

        booking_date,

        "%Y-%m-%d"

    ).date()

    booking_time = datetime.strptime(

        booking_time,

        "%H:%M"

    ).time()

    existing = db.query(

        Appointment

    ).filter(

        and_(

            Appointment.date == booking_date,

            Appointment.time == booking_time,

            Appointment.status == "booked"

        )

    ).first()

    if existing:

        return {

            "success": False,

            "message": "Slot already booked"

        }

    appointment = Appointment(

        user_id=user_id,

        date=booking_date,

        time=booking_time,

        status="booked"

    )

    db.add(appointment)

    db.commit()

    db.refresh(appointment)

    return {

        "success": True,

        "appointment_id": appointment.id,

        "message": "Appointment booked"

    }


def retrieve_appointments(

    db: Session,

    user_id: int

):

    appointments = db.query(

        Appointment

    ).filter(

        Appointment.user_id == user_id

    ).all()

    result = []

    for a in appointments:

        result.append({

            "appointment_id": a.id,

            "date": str(a.date),

            "time": a.time.strftime("%H:%M"),

            "status": a.status

        })

    return {

        "success": True,

        "appointments": result

    }


def cancel_appointment(

    db: Session,

    appointment_id: int

):

    appointment = db.query(

        Appointment

    ).filter(

        Appointment.id == appointment_id

    ).first()

    if not appointment:

        return {

            "success": False,

            "message": "Appointment not found"

        }

    appointment.status = "cancelled"

    db.commit()

    return {

        "success": True,

        "message": "Appointment cancelled"

    }


def modify_appointment(

    db: Session,

    appointment_id: int,

    new_date: str,

    new_time: str

):

    appointment = db.query(

        Appointment

    ).filter(

        Appointment.id == appointment_id

    ).first()

    if not appointment:

        return {

            "success": False,

            "message": "Appointment not found"

        }

    new_date = datetime.strptime(

        new_date,

        "%Y-%m-%d"

    ).date()

    new_time = datetime.strptime(

        new_time,

        "%H:%M"

    ).time()

    existing = db.query(

        Appointment

    ).filter(

        Appointment.date == new_date,

        Appointment.time == new_time,

        Appointment.status == "booked"

    ).first()

    if existing:

        return {

            "success": False,

            "message": "Requested slot unavailable"

        }

    appointment.date = new_date

    appointment.time = new_time

    db.commit()

    db.refresh(appointment)

    return {

        "success": True,

        "message": "Appointment updated"

    }


def end_conversation(

    db: Session,

    session_id: int,

    summary: str

):

    session = db.query(

        ConversationSession

    ).filter(

        ConversationSession.id == session_id

    ).first()

    if not session:

        return {

            "success": False,

            "message": "Session not found"

        }

    session.summary = summary

    db.commit()

    db.refresh(session)

    return {

        "success": True,

        "message": "Conversation ended"

    }