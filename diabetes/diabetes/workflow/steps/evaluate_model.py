from diabetes.workflow import DiabetesStep
from diabetes.workflow.steps.load_model import ModelPredictionStep
from diabetes.workflow.steps.preprocessing_data import DataPreprocessingStep



class ModelEvaluationStep(DiabetesStep):
    def __init__(self):
        pass
    

    def __call__(self, X_test, y_test, model_name, **kwargs):
        
        score = model_name.score(X_test, y_test)

        return{'score': score, **kwargs}