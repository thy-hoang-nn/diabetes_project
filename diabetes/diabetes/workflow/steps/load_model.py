from diabetes.workflow import DiabetesStep, DiabetesWorkflow

import joblib

from diabetes.workflow.tools.classifier import ClassifierSwitcher
import pandas as pd


class ModelPredictionStep(DiabetesStep):
    def __init__(self) -> None:
        pass

    def __call__(self, model_name, data: pd.DataFrame, **kwargs):
        with open(model_name, "rb") as file:
            model = joblib.load(file)
            result = model.predict(data)[0]

            accuracy = model.best_score_

        return {"accuracy": accuracy, "status": result, **kwargs}
