# Weather Monitoring Pipeline

This project tracks weather metrics published by the OpenWeatherMap API, implementing a data pipeline with bronze, silver, and gold data layers.
The purpose of this app was to learn about building a end-to-end project using DuckDb and Streamlit.


## Project Structure
```
air-quality/
├── src/
│   ├── config/
│   ├── ingestion/
│   ├── processing/
│   ├── storage/
│   └── utils/
|   └── visualization/
└── tests/
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
- Copy `.env.example` to `.env`
- Add your API key

## Usage

Run the pipeline:
```bash
python src/main.py
```

## Data Layers

- **Bronze**: Raw data as received from the API
- **Silver**: Cleaned and transformed data
- **Gold**: Analytics-ready data for Streamlit

## Ingestion
Ingest JSON data into DuckDB bronze schema. 

## Transformation
Flatten the JSON raw data into columns

## Gold table
Use aggregates

## Serve Data
Use streamlit to serve data using the command

```
python3 -m streamlit run src/visualization/app.py
```

## Github Actions
Github actions will be used to update the DuckDb file with newer data every hour.