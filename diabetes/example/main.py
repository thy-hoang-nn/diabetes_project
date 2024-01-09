from diabetes.workflow.steps.preprocessing_data import DataPreprocessingStep
from diabetes.workflow.steps.load_model import ModelPredictionStep
from diabetes.workflow.steps.evaluate_model import ModelEvaluationStep

from diabetes.workflow import DiabetesWorkflow

from diabetes.config import MODEL_DIR
from diabetes.config import DATA_DIR
from diabetes.workflow.tools.classifier import ClassifierSwitcher

steps = [ModelPredictionStep()]

workflow = DiabetesWorkflow(steps = steps)



result = workflow(model_name = MODEL_DIR)
print(result["accuracy"])

