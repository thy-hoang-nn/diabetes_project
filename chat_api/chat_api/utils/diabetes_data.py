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
