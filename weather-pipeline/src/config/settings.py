import os
import sys
from pathlib import Path
from dotenv import load_dotenv

print(sys.executable)
# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"

# Data layer paths
BRONZE_DIR = DATA_DIR / "bronze"
SILVER_DIR = DATA_DIR / "silver"
GOLD_DIR = DATA_DIR / "gold"

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openweathermap.org/data/2.5/weather?lat=12.2958&lon=76.63&units=metric")  # Defaults to this if not set
API_KEY = os.getenv("API_KEY") # read key from environment variables

if not API_KEY:
    raise ValueError("API_KEY environment variable not set. Please set it in your .env file.")

