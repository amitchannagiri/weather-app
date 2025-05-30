from ingestion.api_client import WeatherAPI
from storage.data_storage import FileStorage
from processing.data_processor import DataProcessor
import logging


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def main():
    logger = setup_logging()
    
    try:
        # Initialize components
        api_client = WeatherAPI()
        storage = FileStorage()
        processor = DataProcessor()

        # Fetch and store raw data (Bronze)
        logger.info("Fetching raw data...")
        raw_data = api_client.fetch_city_weather_data()
        conn = storage.save_to_bronze(raw_data)
        logger.info("Saved bronze data to duckdb")

        # print("Stored Weather Data:")
        # df = conn.execute("SELECT * FROM weather_data_bronze").df()
        # print(df)
        # conn.close()

        # Process and store silver data
        logger.info("Processing silver layer...")
        bronze_df = conn.execute("describe table weather_data_bronze").df()
        # print(bronze_df)
        silver_data = processor.process_silver(bronze_df)
        conn = storage.save_to_silver()
        logger.info("Saved silver data to silver table")
        # silver_data_processed = conn.execute("SELECT * FROM weather_data_silver").df()
        # print(silver_data_processed)

        # Process and store gold data
        logger.info("Processing gold layer...")
        gold_data = processor.process_gold(silver_data)
        print(gold_data)
        gold_path_conn = storage.save_to_gold()
        gold_path_conn.close()
        logger.info("Saved gold data to gold table")

    except Exception as e:
        logger.error("Error in pipeline: %s", str(e))
        raise

if __name__ == "__main__":
    main()