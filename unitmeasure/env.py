import os

class AppEnv:
    LOGGING_LEVEL: str = os.getenv("LOGGING_LEVEL", "INFO")