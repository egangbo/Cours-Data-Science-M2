from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import pandas as pd
import os

CITIES = {
    "Paris": {"latitude": 48.85, "longitude": 2.35},
    "London": {"latitude": 51.51, "longitude": -0.13},
    "Berlin": {"latitude": 52.52, "longitude": 13.41},
}

CSV_PATH = r"C:\Users\Gbemissola\Documents\Master2\DataScience\Cours-Data-Science-M2\Airflow\projet\weather_data.csv"


def extract_weather_data():
    results = []
    for city, coords in CITIES.items():
        url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['latitude']}&longitude={coords['longitude']}&current_weather=true"
        response = requests.get(url)
        data = response.json().get('current_weather', {})
        results.append({
            "city": city,
            "temperature": data.get("temperature"),
            "windspeed": data.get("windspeed"),
            "weathercode": data.get("weathercode"),
            "timestamp": datetime.utcnow().isoformat()
        })
    return results

def transform_and_load(weather_data):
    df = pd.DataFrame(weather_data)
    os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
    if os.path.exists(CSV_PATH):
        existing_df = pd.read_csv(CSV_PATH)
        combined_df = pd.concat([existing_df, df], ignore_index=True).drop_duplicates()
        combined_df.to_csv(CSV_PATH, index=False)
    else:
        df.to_csv(CSV_PATH, index=False)

with DAG(
    dag_id='daily_weather_etl',
    start_date=datetime(2024, 1, 1),
    schedule_interval='0 8 * * *',
    catchup=False,
    tags=['weather'],
) as dag:

    extract_task = PythonOperator(
        task_id='extract_weather',
        python_callable=extract_weather_data
    )

    transform_load_task = PythonOperator(
        task_id='transform_and_load_weather',
        python_callable=transform_and_load,
        op_args=[extract_task.output]
    )

    extract_task >> transform_load_task
