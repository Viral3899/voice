from fastapi import FastAPI

from database import Base
from database import engine
from routes.voice import router as voice_router
from routes.appointments import router as appointments_router


# -------------------------
# Create DB Tables
# -------------------------

Base.metadata.create_all(bind=engine)


# -------------------------
# FastAPI App
# -------------------------

app = FastAPI(

    title="Voice AI Appointment Agent",

    version="1.0.0"

)


# -------------------------
# Routers
# -------------------------

app.include_router(voice_router)

app.include_router(appointments_router)


# -------------------------
# Health Check
# -------------------------

@app.get("/")

def health_check():

    return {

        "status": "ok",

        "message": "Voice AI Backend Running"

    }


@app.get("/health")

def health():

    return {

        "status": "healthy"

    }

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)