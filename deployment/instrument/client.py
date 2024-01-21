from time import sleep

import requests
from loguru import logger

json_data = {
    "Pregnancies": 5,
    "Glucose": 120,
    "BloodPressure": 80,
    "SkinThickness": 30,
    "Insulin": 50,
    "BMI": 25.5,
    "DiabetesPedigreeFunction": 0.5,
    "Age": 35,
}


def predict():
    logger.info("Sending POST requests!")

    response = requests.post(
        "http://0.0.0.0:8098/predict",
        headers={
            "accept": "application/json",
        },
        json=json_data,
    )
    if response.status_code == 200:
        logger.info("Request successful")
    else:
        logger.error(f"Request failed with status code {response.status_code}")


if __name__ == "__main__":
    while True:
        predict()
        sleep(1)
