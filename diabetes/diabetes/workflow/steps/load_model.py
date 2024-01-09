from diabetes.workflow import DiabetesStep, DiabetesWorkflow

import joblib

from diabetes.workflow.tools.classifier import ClassifierSwitcher


  

class ModelPredictionStep(DiabetesStep):
    def __init__(self) -> None:
        pass    

    def __call__(self, model_name,  **kwargs):
        with open(model_name, 'rb') as file:
            model = joblib.load(file)
           
            accuracy = model.best_score_
            
        return {'accuracy': accuracy,  **kwargs}



