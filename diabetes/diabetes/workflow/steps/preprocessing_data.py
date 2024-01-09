from diabetes.workflow import DiabetesStep
import pandas as pd
import numpy as np
from imblearn.over_sampling import RandomOverSampler
from sklearn.model_selection import train_test_split

class DataPreprocessingStep(DiabetesStep):
    def __call__(self, file, **kwargs):
        data = pd.read_csv(file)

        # columns_to_replace= data[['Glucose','BloodPressure','SkinThickness','Insulin','BMI']]
        data[['Glucose','BloodPressure','SkinThickness','Insulin','BMI']] = data[['Glucose','BloodPressure','SkinThickness','Insulin','BMI']].replace(0,np.NaN)
        data['Glucose'].fillna(data['Glucose'].mean(), inplace = True)
        data['BloodPressure'].fillna(data['BloodPressure'].mean(), inplace = True)
        data['SkinThickness'].fillna(data['SkinThickness'].median(), inplace = True)
        data['Insulin'].fillna(data['Insulin'].median(), inplace = True)
        data['BMI'].fillna(data['BMI'].median(), inplace = True)

        data['Age_Pregnancy_Ratio'] = data['Age'] * data['Pregnancies']

        data['SkinThickness_BMI_Product'] = data['SkinThickness'] * data['BMI']

        data_train = data.drop(['DiabetesPedigreeFunction', 'SkinThickness', 'Pregnancies', 'BMI', 'BloodPressure'], axis=1)

        y = data_train.pop('Outcome')
      
        ros = RandomOverSampler(random_state=42)
        X_resampled, y_resampled = ros.fit_resample(data_train, y)
        
        X_train, X_test, y_train, y_test = train_test_split(X_resampled,y_resampled, test_size=0.2, random_state=42)

        return {'X_test': X_test, 'y_test': y_test, **kwargs}



   

