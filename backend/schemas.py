from pydantic import BaseModel


class UserCreate(BaseModel):

    phone_number: str

    name: str


class AppointmentCreate(BaseModel):

    user_id: int

    date: str

    time: str


class AppointmentUpdate(BaseModel):

    appointment_id: int

    new_date: str

    new_time: str


class MessageRequest(BaseModel):

    session_id: int

    text: str


class TTSRequest(BaseModel):

    text: str


class SummaryResponse(BaseModel):

    summary: str