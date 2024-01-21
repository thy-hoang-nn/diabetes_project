# Read more about OpenTelemetry here:
# https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/fastapi/fastapi.html

from fastapi import FastAPI
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import get_tracer_provider, set_tracer_provider
from chat_api.classifier import ClassifierSwitcher


from diabetes.workflow import DiabetesWorkflow
from diabetes.workflow.steps.preprocessing_data import DataPreprocessingStep
from diabetes.workflow.steps.load_model import ModelPredictionStep

from diabetes.config import PACKAGE_DIR, MODEL_DIR


from fastapi import status, APIRouter
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn

from loguru import logger
import os

set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "diabetes-prediction-service"})
    )
)
tracer = get_tracer_provider().get_tracer("diabetes-prediction", "1.0.0")

jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)
span_processor = BatchSpanProcessor(jaeger_exporter)
get_tracer_provider().add_span_processor(span_processor)

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
async def get_pima_accuracy(model_path: UploadFile = File(...)):
    try:
        if model_path:
            model_name = os.path.join(
                PACKAGE_DIR, "models", model_path.filename
            )

            logger.info("Make prediction...")
            result = prediction_workflow(model_name=model_name)

            # Add histogram

            return {"result": result["accuracy"]}
        else:
            return {"error": "No file provided for evaluation"}
    except Exception as e:
        return {
            "error": str(e),
            "model_path": getattr(model_path, "filename", None),
        }


if __name__ == "__main__":
    FastAPIInstrumentor.instrument_app(app)
    uvicorn.run(app, host="0.0.0.0", port=8089)
