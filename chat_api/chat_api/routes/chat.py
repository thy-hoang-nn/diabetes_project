from fastapi import status, APIRouter
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse

from loguru import logger
from fastapi.encoders import jsonable_encoder
import pandas as pd


from chat_api.classifier import ClassifierSwitcher


from diabetes.workflow import DiabetesWorkflow
from diabetes.workflow.steps.preprocessing_data import DataPreprocessingStep
from diabetes.workflow.steps.load_model import ModelPredictionStep

from diabetes.config import PACKAGE_DIR, MODEL_DIR
from chat_api.utils.diabetes_data import Diabetes_data


preprocessing_workflow = DiabetesWorkflow(steps=[DataPreprocessingStep()])
prediction_workflow = DiabetesWorkflow(steps=[ModelPredictionStep()])


# Class to define the request body


router = APIRouter()

uploaded_dataset = None


@router.get(
    "/health",
    name="Get non-stream chat response",
)
def health_check():
    return JSONResponse(True, 200)


@router.post(
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
        return {"result": "File uploaded successfully"}
    except Exception as e:
        return {"error": str(e)}


@router.post(
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


@router.post(
    "/predict",
    name="predict the onset of pima diabetes",
    status_code=status.HTTP_200_OK,
)
async def get_pima_accuracy(data: Diabetes_data):
    logger.info("Making predictions...")
    logger.info(jsonable_encoder(data))
    logger.info(pd.DataFrame(jsonable_encoder(data), index=[0]))

    result = prediction_workflow(
        model_name=MODEL_DIR,
        data=pd.DataFrame(jsonable_encoder(data), index=[0]),
    )
    prediction_label = "Normal" if result["status"] == 0 else "Diabetes"

    return {"result": prediction_label}
