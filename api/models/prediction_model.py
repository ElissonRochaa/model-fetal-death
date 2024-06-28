from xgboost import XGBClassifier  # ou XGBRegressor, dependendo do seu modelo
from datetime import datetime
import pickle
from api.models.custom_model import CustomModel

def predict_test(X_test, custom_model):

    y_pred = custom_model.model.predict(X_test)
    y_proba = custom_model.model.predict_proba(X_test)
    result = {
            'prediction': int(y_pred[0]), #predição da classe alvo
            'probability': {
                '0': float(y_proba[0][0]), #predição da probabilidade de ser 0
                '1': float(y_proba[0][1]) #predição da probabilidade de ser 1 #TALVEZ É PORCENTAGEM
            }
        }
    return result

# Função para carregar o modelo do arquivo pickle
def load_model():

    with open("api/models/fetal_death_model.pkl", "rb") as f:
        my_class = pickle.load(f)
    return my_class