from dotenv import load_dotenv
import os

load_dotenv()


class Settings:

    DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

    CARTESIA_API_KEY = os.getenv("CARTESIA_API_KEY")

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///./voice_ai.db"
    )

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    GROQ_MODEL = os.getenv(
        "GROQ_MODEL",
        "llama-3.1-8b-instant"
    )

    MAX_HISTORY = int(
        os.getenv(
            "MAX_HISTORY",
            10
        )
    )


settings = Settings()