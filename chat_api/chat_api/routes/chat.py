from fastapi import status, APIRouter
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
import os







from diabetes.workflow import DiabetesWorkflow
from diabetes.workflow.steps.preprocessing_data import DataPreprocessingStep
from diabetes.workflow.steps.load_model import ModelPredictionStep

from diabetes.config import PACKAGE_DIR, MODEL_DIR
from chat_api.classifier import ClassifierSwitcher




preprocessing_workflow = DiabetesWorkflow(steps = [DataPreprocessingStep()])
prediction_workflow = DiabetesWorkflow(steps = [ModelPredictionStep()])


router = APIRouter()

uploaded_dataset = None



@router.post("/upload", name = "upload dataset file", status_code = status.HTTP_200_OK)
async def upload_dataset_file(dataset_path: UploadFile = File(...)):
    global uploaded_dataset
    try:
        # Save the uploaded file
        with open(dataset_path.filename, "wb") as file:
            file.write(dataset_path.file.read())
        # Store the uploaded dataset globally
        uploaded_dataset = dataset_path.filename
        return {'result': 'File uploaded successfully'}
    except Exception as e:
        return {'error': str(e)}
   

@router.post("/query/preprocessing", name="preprocessing pima dataset", status_code = status.HTTP_200_OK)
async def preprocessing_pima_dataset():
    global uploaded_dataset
    try:
        if uploaded_dataset:
            # Process the globally stored dataset
            result = preprocessing_workflow(file=uploaded_dataset)

            X_test_json = result['X_test'].to_json(orient='split', index=False)
            y_test_json = result['y_test'].to_json(orient='split', index=False)


            return {'X_test': X_test_json, 'y_test': y_test_json}
        
        else:
            return JSONResponse(content={'error': 'No dataset uploaded for preprocessing.'}, status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JSONResponse(content={'error': str(e)}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# @router.post("/query/perfomance", name="predict the onset of pima diabetes", status_code = status.HTTP_200_OK)

# async def get_pima_accuracy(model_path: UploadFile=File(...)):
#     try:
#         if model_path:
#             model_name = os.path.join(PACKAGE_DIR, "models", model_path.filename)
#             result = prediction_workflow(model_name=model_name)
#             return {'result': result['accuracy']}
#         else:
#             return {'error': 'No file provided for evaluation'}
#     except Exception as e:
#         return {'error': str(e),
#                 'model_path': getattr(model_path, 'filename', None)}
    

@router.post("/query/perfomance", name="predict the onset of pima diabetes", status_code = status.HTTP_200_OK)   

async def get_pima_accuracy():
    result = prediction_workflow(model_name = MODEL_DIR)
    return {'result': result['accuracy']}
    




           
      
    
    
    

