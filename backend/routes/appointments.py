from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from database import get_db

from schemas import (
    AppointmentCreate,
    AppointmentUpdate
)

from tools import (
    book_appointment,
    retrieve_appointments,
    cancel_appointment,
    modify_appointment
)


router = APIRouter(

    prefix="/api/appointments",

    tags=["Appointments"]

)


# -------------------------
# Get Appointments
# -------------------------

@router.get("/{user_id}")

def get_appointments(

    user_id: int,

    db: Session = Depends(get_db)

):

    result = retrieve_appointments(

        db,

        user_id

    )

    return result



# -------------------------
# Book Appointment
# -------------------------

@router.post("/book")

def create_appointment(

    payload: AppointmentCreate,

    db: Session = Depends(get_db)

):

    result = book_appointment(

        db=db,

        user_id=payload.user_id,

        booking_date=payload.date,

        booking_time=payload.time

    )


    if not result["success"]:

        raise HTTPException(

            status_code=400,

            detail=result["message"]

        )


    return result



# -------------------------
# Modify Appointment
# -------------------------

@router.put("/modify")

def update_appointment(

    payload: AppointmentUpdate,

    db: Session = Depends(get_db)

):

    result = modify_appointment(

        db=db,

        appointment_id=payload.appointment_id,

        new_date=payload.new_date,

        new_time=payload.new_time

    )


    if not result["success"]:

        raise HTTPException(

            status_code=400,

            detail=result["message"]

        )


    return result



# -------------------------
# Cancel Appointment
# -------------------------

@router.delete("/{appointment_id}")

def delete_appointment(

    appointment_id: int,

    db: Session = Depends(get_db)

):

    result = cancel_appointment(

        db,

        appointment_id

    )


    if not result["success"]:

        raise HTTPException(

            status_code=404,

            detail=result["message"]

        )


    return result