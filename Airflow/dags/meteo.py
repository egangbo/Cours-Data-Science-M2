from airflow import DAG
from airflow.decorators import task
from airflow.utils.dates import days_ago
import requests
import pandas as pd
from datetime import datetime
import os

# Define cities with lat/lon
CITIES = {
    "Paris": {"latitude": 48.85, "longitude": 2.35},
    "London": {"latitude": 51.51, "longitude": -0.13},
    "Berlin": {"latitude": 52.52, "longitude": 13.41},
}

CSV_PATH = r"C:\Users\Gbemissola\Documents\Master2\DataScience\Cours-Data-Science-M2\Airflow\data\weather_data.csv"


default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "retries": 1,
}


with DAG(
    dag_id="daily_weather_etl",
    schedule_interval="0 8 * * *",  # 8 AM UTC daily
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=["weather", "etl"],
) as dag:

    @task()
    def extract():
        results = []
        for city, coords in CITIES.items():
            url = (
                f"https://api.open-meteo.com/v1/forecast"
                f"?latitude={coords['latitude']}&longitude={coords['longitude']}&current_weather=true"
            )
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            current = data.get("current_weather", {})
            results.append(
                {
                    "city": city,
                    "temperature_c": current.get("temperature"),
                    "windspeed_kmh": current.get("windspeed"),
                    "weather_code": current.get("weathercode"),
                    "timestamp": datetime.utcnow(),
                }
            )
        return results

    @task()
    def transform(raw_data: list):
        # Convert list of dicts to DataFrame
        df = pd.DataFrame(raw_data)

        # Format timestamp to ISO string
        df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%SZ")

        # Clean/normalize if needed (already simple structure)
        return df

    @task()
    def load(df: pd.DataFrame):
        # Ensure folder exists
        os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)

        if os.path.exists(CSV_PATH):
            existing_df = pd.read_csv(CSV_PATH)

            # Avoid duplicates based on city & timestamp
            merged = pd.concat([existing_df, df], ignore_index=True)
            merged.drop_duplicates(subset=["city", "timestamp"], inplace=True)
            merged.to_csv(CSV_PATH, index=False)
        else:
            df.to_csv(CSV_PATH, index=False)

    raw = extract()
    transformed = transform(raw)
    load(transformed)
