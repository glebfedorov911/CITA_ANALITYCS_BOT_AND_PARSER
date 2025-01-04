from dotenv import load_dotenv
import os


load_dotenv()

URL = os.getenv("URL")
ECHO = os.getenv("ECHO") == "True"