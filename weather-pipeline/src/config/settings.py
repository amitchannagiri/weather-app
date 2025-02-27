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
API_BASE_URL = "https://api.openweathermap.org/data/2.5/weather?lat=12.2958&lon=76.63"
API_KEY = "c625d285d05b740f00dd429438e51712"