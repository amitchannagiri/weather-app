import sys
sys.path.append("..")
from pathlib import Path
import duckdb
import json

class FileStorage:
    @staticmethod
    def _ensure_db(name: str):
        """Ensure the database exists and tables are created if they do not exists"""
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
        #table silver
        conn.execute("""
                        CREATE TABLE IF NOT EXISTS weather_data_silver (
                            id INTEGER PRIMARY KEY,
                            coord_lon REAL,
                            coord_lat REAL,
                            weather_id INTEGER,
                            weather_main VARCHAR,
                            weather_description VARCHAR,
                            weather_icon VARCHAR,
                            base VARCHAR,
                            main_temp REAL,
                            main_feels_like REAL,
                            main_temp_min REAL,
                            main_temp_max REAL,
                            main_pressure INTEGER,
                            main_humidity INTEGER,
                            visibility INTEGER,
                            wind_speed REAL,
                            wind_deg REAL,
                            clouds_all INTEGER,
                            dt INTEGER,
                            sys_type VARCHAR,
                            sys_id INTEGER,
                            sys_country VARCHAR,
                            sys_sunrise INTEGER,
                            sys_sunset INTEGER,
                            timezone INTEGER,
                            city_id INTEGER,
                            city_name VARCHAR
                        );
                         """)
        #table gold
        conn.execute("""
                        CREATE TABLE IF NOT EXISTS weather_data_gold (
                            id INTEGER PRIMARY KEY,
                            coord_lon REAL,
                            coord_lat REAL,
                            weather_id INTEGER,
                            weather_main VARCHAR,
                            weather_description VARCHAR,
                            weather_icon VARCHAR,
                            base VARCHAR,
                            main_temp REAL,
                            main_feels_like REAL,
                            main_temp_min REAL,
                            main_temp_max REAL,
                            main_pressure INTEGER,
                            main_humidity INTEGER,
                            visibility INTEGER,
                            wind_speed REAL,
                            wind_deg REAL,
                            clouds_all INTEGER,
                            dt INTEGER,
                            sys_type VARCHAR,
                            sys_id INTEGER,
                            sys_country VARCHAR,
                            sys_sunrise INTEGER,
                            sys_sunset INTEGER,
                            timezone INTEGER,
                            city_id INTEGER,
                            city_name VARCHAR)
                     """
                        )
        return conn
    def save_to_bronze(self, data: str) -> Path:
        """Save raw data to bronze layer"""
        conn = self._ensure_db("weather.duckdb")
        raw_data = json.dumps(data)
        conn.execute("INSERT INTO weather_data_bronze (id,raw_json) VALUES (nextval('seq_bronze_id'),(?))",[raw_data])
        return conn

    def save_to_silver(self) -> Path:
        """Save processed data to silver layer"""
        conn = self._ensure_db("weather.duckdb")
        conn.execute("""
                     INSERT INTO weather_data_silver
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
                    FROM weather_data_bronze
                    WHERE id NOT IN (SELECT id FROM weather_data_silver);
                     """)
        return conn

    def save_to_gold(self) -> Path:
        """Save analytics-ready data to gold layer"""
        conn = self._ensure_db("weather.duckdb")
        conn.execute("""
            INSERT INTO weather_data_gold
            SELECT * FROM weather_data_silver
            WHERE id NOT IN (SELECT id FROM weather_data_gold);
        """)
        return conn
