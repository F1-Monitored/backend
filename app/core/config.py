from dotenv import load_dotenv
import os

load_dotenv()

FASTF1_CACHE = os.getenv("FASTF1_CACHE", "./cache")