from fastapi import APIRouter
from fastapi import Depends
from fastapi import UploadFile
from fastapi import File
from fastapi import HTTPException
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from database import get_db

from models import ConversationSession

from schemas import MessageRequest
from schemas import TTSRequest

from llm import process_message

from voice import (
    speech_to_text,
    text_to_speech
)

from tools import end_conversation


router = APIRouter(
    prefix="/api/voice",
    tags=["Voice"]
)


# -------------------------
# Start Session
# -------------------------

@router.post("/start-session")

def start_session(

    db: Session = Depends(get_db)

):

    session = ConversationSession(

        transcript="",

        summary=""

    )

    db.add(session)

    db.commit()

    db.refresh(session)

    return {

        "success": True,

        "session_id": session.id

    }



# -------------------------
# Speech To Text
# -------------------------

@router.post("/transcribe")

async def transcribe_audio(

    audio: UploadFile = File(...)

):

    try:

        result = await speech_to_text(

            audio

        )

        return result

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )



# -------------------------
# LLM + Tool Calling
# -------------------------

@router.post("/process-message")

def process_user_message(

    payload: MessageRequest,

    db: Session = Depends(get_db)

):

    session = db.query(

        ConversationSession

    ).filter(

        ConversationSession.id

        == payload.session_id

    ).first()


    if not session:

        raise HTTPException(

            status_code=404,

            detail="Session not found"

        )


    history = []

    if session.transcript:

        history = eval(

            session.transcript

        )


    response = process_message(

        db=db,

        message=payload.text,

        history=history

    )


    history.append({

        "role":"user",

        "content":payload.text

    })


    history.append({

        "role":"assistant",

        "content":

        response["response"]

    })


    history = history[-10:]


    session.transcript = str(

        history

    )

    db.commit()


    return {

        "success": True,

        "response":

        response["response"],

        "tool":

        response.get("tool"),

        "tool_result":

        response.get(

            "tool_result"

        )

    }



# -------------------------
# Text To Speech
# -------------------------

@router.post("/synthesize")

def synthesize_audio(

    payload: TTSRequest

):

    result = text_to_speech(

        payload.text

    )


    if not result["success"]:

        raise HTTPException(

            status_code=500,

            detail=result["message"]

        )


    return FileResponse(

        result["audio_file"],

        media_type="audio/wav",

        filename="response.wav"

    )



# -------------------------
# End Session
# -------------------------

@router.post("/end-session/{session_id}")

def finish_session(

    session_id: int,

    db: Session = Depends(get_db)

):

    session = db.query(

        ConversationSession

    ).filter(

        ConversationSession.id

        == session_id

    ).first()


    if not session:

        raise HTTPException(

            status_code=404,

            detail="Session not found"

        )


    summary = f"""

Session ID: {session.id}

Transcript:

{session.transcript}

"""


    result = end_conversation(

        db=db,

        session_id=session_id,

        summary=summary

    )


    return {

        "success": True,

        "summary":

        summary,

        "message":

        result["message"]

    }