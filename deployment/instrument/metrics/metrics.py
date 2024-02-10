import uvicorn
from fastapi import FastAPI

from fastapi import status, APIRouter
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
from time import time

from loguru import logger
from opentelemetry import metrics
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.metrics import set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from prometheus_client import start_http_server


from chat_api.classifier import ClassifierSwitcher
from fastapi.encoders import jsonable_encoder
import pandas as pd


from diabetes.workflow import DiabetesWorkflow
from diabetes.workflow.steps.preprocessing_data import DataPreprocessingStep
from diabetes.workflow.steps.load_model import ModelPredictionStep

from diabetes.config import PACKAGE_DIR, MODEL_DIR


from pydantic import BaseModel
from typing import Optional


class Diabetes_data(BaseModel):
    Pregnancies: int
    Glucose: int
    BloodPressure: Optional[int] = None
    SkinThickness: int
    Insulin: Optional[int] = None
    BMI: float
    DiabetesPedigreeFunction: Optional[float] = None
    Age: int


start_http_server(port=8099, addr="0.0.0.0")

resource = Resource(attributes={SERVICE_NAME: "diabetes-prediction-service"})

reader = PrometheusMetricReader()

provider = MeterProvider(resource=resource, metric_readers=[reader])
set_meter_provider(provider)
meter = metrics.get_meter("diabetes-prediction", "0.1.2")


# Create your first counter
counter = meter.create_counter(
    name="app_request_counter", description="Number of app requests"
)

histogram = meter.create_histogram(
    name="app_response_histogram",
    description="App response histogram",
    unit="seconds",
)


preprocessing_workflow = DiabetesWorkflow(steps=[DataPreprocessingStep()])
prediction_workflow = DiabetesWorkflow(steps=[ModelPredictionStep()])


app = FastAPI()

uploaded_dataset = None


@app.post(
    "/upload", name="upload dataset file", status_code=status.HTTP_200_OK
)
async def upload_dataset_file(dataset_path: UploadFile = File(...)):
    global uploaded_dataset
    try:
        # Save the uploaded file
        with open(dataset_path.filename, "wb") as file:
            file.write(dataset_path.file.read())
        # Store the uploaded dataset globally
        uploaded_dataset = dataset_path.filename

        logger.info("Data is uploading")
        logger.info(uploaded_dataset)
        return {"result": "File uploaded successfully"}
    except Exception as e:
        return {"error": str(e)}


@app.post(
    "/preprocessing",
    name="preprocessing pima dataset",
    status_code=status.HTTP_200_OK,
)
async def preprocessing_pima_dataset():
    global uploaded_dataset
    try:
        if uploaded_dataset:
            # Process the globally stored dataset

            result = preprocessing_workflow(file=uploaded_dataset)

            X_test_json = result["X_test"].to_json(orient="split", index=False)
            y_test_json = result["y_test"].to_json(orient="split", index=False)

            return {"X_test": X_test_json, "y_test": y_test_json}

        else:
            return JSONResponse(
                content={"error": "No dataset uploaded for preprocessing."},
                status_code=status.HTTP_400_BAD_REQUEST,
            )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@app.post(
    "/predict",
    name="predict the onset of pima diabetes",
    status_code=status.HTTP_200_OK,
)
async def get_pima_accuracy(data: Diabetes_data):
    starting_time = time()
    logger.info("Making predictions...")
    logger.info(jsonable_encoder(data))
    logger.info(pd.DataFrame(jsonable_encoder(data), index=[0]))

    result = prediction_workflow(
        model_name=MODEL_DIR,
        data=pd.DataFrame(jsonable_encoder(data), index=[0]),
    )
    prediction_label = "Normal" if result["status"] == 0 else "Diabetes"

    label = {"api": "/predict"}

    # Increase the counter
    counter.add(1, label)

    # Mark the end of the response
    ending_time = time()
    elapsed_time = ending_time - starting_time

    # Add histogram
    logger.info("elapsed time: ", elapsed_time)
    logger.info(elapsed_time)
    histogram.record(elapsed_time, label)

    return {"result": prediction_label}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8088)
