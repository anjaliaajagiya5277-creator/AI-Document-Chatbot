import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "dev-secret-key"
    )

    GOOGLE_API_KEY = os.getenv(
        "GOOGLE_API_KEY"
    )

    MODEL_NAME = os.getenv(
        "MODEL_NAME",
        "gemini-2.5-flash"
    )

    UPLOAD_FOLDER = os.getenv(
        "UPLOAD_FOLDER",
        "uploads"
    )

    MAX_CONTENT_LENGTH = int(
        os.getenv(
            "MAX_CONTENT_LENGTH",
            50 * 1024 * 1024
        )
    )

    ALLOWED_EXTENSIONS = {
        "pdf",
        "ppt",
        "pptx"
    }