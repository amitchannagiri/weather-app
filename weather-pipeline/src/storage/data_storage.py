import sys
sys.path.append("..")
import pandas as pd
from datetime import datetime
from pathlib import Path
from config.settings import BRONZE_DIR, SILVER_DIR, GOLD_DIR
import duckdb
import json

class FileStorage:
    @staticmethod
    def _ensure_directory(directory: Path):
        """Ensure the directory exists"""
        directory.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _ensure_db(name: str):
        """Ensure the database exists"""
        conn = duckdb.connect(name)

        # Create Weather Data Table
        conn.execute("""
        CREATE TABLE IF NOT EXISTS weather_data_bronze (
            id INTEGER PRIMARY KEY,
            raw_json JSON
        );
        """)
        conn.execute("""
                     CREATE SEQUENCE IF NOT EXISTS seq_bronze_id START 1;
                     """)
        return conn

    def save_to_bronze(self, data: str) -> Path:
        """Save raw data to bronze layer"""
        self._ensure_directory(BRONZE_DIR)
        conn = self._ensure_db("weather.duckdb")
        raw_data = json.dumps(data)
        conn.execute("INSERT INTO weather_data_bronze (id,raw_json) VALUES (nextval('seq_bronze_id'),(?))",[raw_data])
        return conn

    def save_to_silver(self, data: pd.DataFrame) -> Path:
        """Save processed data to silver layer"""
        conn = self._ensure_db("weather.duckdb")
        conn.execute("""
                     CREATE TABLE IF NOT EXISTS weather_data_silver AS 
                     SELECT 
                        id, 
                        json_extract_string(raw_json, '$.coord_lon') AS coord_lon,
                        json_extract_string(raw_json, '$.coord_lat') AS coord_lat,
                        json_extract_string(raw_json, '$.weather_0_id') AS weather_id,
                        json_extract_string(raw_json, '$.weather_0_main') AS weather_main,
                        json_extract_string(raw_json, '$.weather_0_description') AS weather_description,
                        json_extract_string(raw_json, '$.weather_0_icon') AS weather_icon,
                        json_extract_string(raw_json, '$.base') AS base,
                        json_extract_string(raw_json, '$.main_temp') AS main_temp,
                        json_extract_string(raw_json, '$.main_feels_like') AS main_feels_like,
                        json_extract_string(raw_json, '$.main_temp_min') AS main_temp_min,
                        json_extract_string(raw_json, '$.main_temp_max') AS main_temp_max,
                        json_extract_string(raw_json, '$.main_pressure') AS main_pressure,
                        json_extract_string(raw_json, '$.main_humidity') AS main_humidity,
                        json_extract_string(raw_json, '$.visibility') AS visibility,
                        json_extract_string(raw_json, '$.wind_speed') AS wind_speed,
                        json_extract_string(raw_json, '$.wind_deg') AS wind_deg,
                        json_extract_string(raw_json, '$.clouds_all') AS clouds_all,
                        json_extract_string(raw_json, '$.dt') AS dt,
                        json_extract_string(raw_json, '$.sys_type') AS sys_type,
                        json_extract_string(raw_json, '$.sys_id') AS sys_id,
                        json_extract_string(raw_json, '$.sys_country') AS sys_country,
                        json_extract_string(raw_json, '$.sys_sunrise') AS sys_sunrise, 
                        json_extract_string(raw_json, '$.sys_sunset') AS sys_sunset,
                        json_extract_string(raw_json, '$.timezone') AS timezone,
                        json_extract_string(raw_json, '$.id') AS city_id,
                        json_extract_string(raw_json, '$.name') AS city_name
                    FROM weather_data_bronze;
                     """)
        return conn

    def save_to_gold(self, data: pd.DataFrame) -> Path:
        """Save analytics-ready data to gold layer"""
        conn = self._ensure_db("weather.duckdb")
        conn.execute("CREATE TABLE IF NOT EXISTS weather_data_gold AS SELECT * FROM weather_data_silver")
        return conn