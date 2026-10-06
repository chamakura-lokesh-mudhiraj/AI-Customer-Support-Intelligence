import os

from dotenv import load_dotenv


load_dotenv()


APP_NAME = os.getenv(
    "APP_NAME",
    "AI Customer Support Intelligence",
)

APP_ENV = os.getenv(
    "APP_ENV",
    "development",
)

DEBUG = os.getenv(
    "DEBUG",
    "True",
).lower() == "true"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-6-luna",
)