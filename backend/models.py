from sqlalchemy import Column

from sqlalchemy import Integer

from sqlalchemy import String

from sqlalchemy import Date

from sqlalchemy import Time

from sqlalchemy import Text

from sqlalchemy import DateTime

from sqlalchemy import ForeignKey

from sqlalchemy.sql import func

from sqlalchemy.orm import relationship

from database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    phone_number = Column(
        String,
        unique=True,
        index=True
    )

    name = Column(String)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    appointments = relationship(
        "Appointment",
        back_populates="user"
    )


class Appointment(Base):

    __tablename__ = "appointments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    date = Column(
        Date,
        index=True
    )

    time = Column(
        Time,
        index=True
    )

    status = Column(
        String,
        default="booked"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    user = relationship(
        "User",
        back_populates="appointments"
    )


class ConversationSession(Base):

    __tablename__ = "conversation_sessions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        nullable=True
    )

    transcript = Column(
        Text,
        default=""
    )

    summary = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )