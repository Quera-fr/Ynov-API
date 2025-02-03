from fastapi import FastAPI, File, UploadFile

tags = [
    {
        'name' : 'Maths',
        'description' : 'Operations related to Maths'
    },
    {
        'name' : 'Models',
        'description' : 'Operations related to Models'
    }
]

app = FastAPI(
    title="My FastAPI App",
    description="This is a simple app",
    version="0.0.1",
    openapi_tags=tags
)

@app.get("/", tags=['Models'])
def default_root():
    return "Hello World"

@app.get("/square", tags=['Maths'])
def square(n:int=1) -> str:
    return n*n

from pydantic import BaseModel

class Data(BaseModel):
    name:str='Kevin'
    city:str='Paris'


@app.post('/formulaire')
def formulaire(data:Data):
    
    data = dict(data)

    name = data['name']
    city = data['city']

    return f"Hello {name} from {city}."


from fastapi import File, UploadFile

@app.post('/upload')
def upload_file(file:UploadFile=File(...)):
    return file.filename



# 0 Chargement du modèle

import pandas as pd
import mlflow, os


os.environ['AWS_ACCESS_KEY_ID'] = ""
os.environ['AWS_SECRET_ACCESS_KEY'] = ""

mlflow.set_tracking_uri("https://quera-server-mlflow-cda209265623.herokuapp.com/")

path = mlflow.MlflowClient().get_registered_model('Ever_Married').latest_versions[0].source
model = mlflow.pyfunc.load_model(path)



# 1 Création d'une structure de données
class User(BaseModel):
    Gender:str= 'Male'
    Age:int= 22
    Graduated:str= 'No'
    Profession:str= 'Healthcare'
    Work_Experience:float= 1.0
    Spending_Score:str= 'Low'
    Family_Size:float= 4.0
    Segmentation:str= 'D'

# 2 Création du EndPoint 'predict' qui utilise la structure de données
@app.post('/predict', tags=['Models'])
def predict(data:User):

    user = pd.DataFrame([dict(data)])
    y_pred = model.predict(user)[0]

    # 3 Retour de la prédiction du modèle (int)
    return int(y_pred)


@app.post('/predict_file')
def predict_file(file:UploadFile=File(...)):
    
    df = pd.read_csv(file.file)

    if 'Gender' not in df.columns or 'Graduated' not in df.columns:
        return False
    
    else :
        X = df.drop(["Ever_Married"], axis=1).dropna()
        y_pred = model.predict(X)
        print (y_pred)
        return [int(n) for n in model.predict(X)]
    

from io import BytesIO
from PIL import Image
import numpy as np


from io import BytesIO
from PIL import Image
import numpy as np
path = mlflow.MlflowClient().get_registered_model('Tensoflow Model Mnist')._latest_version[0].source

model_loaded = mlflow.pyfunc.load_model(path)
@app.post('/predict_digit')
def predict_digit(file:UploadFile=File(...)):

    # Décodage de l'image
    img = Image.open(BytesIO(file.file.read()))

    # Resize et normalisation de l'image
    img = (255 - np.array(img.resize((28,28)).convert('L')))/255
    img = img.reshape(-1, 28,28,1)
    
    
    return {'Prediction': int(model_loaded.predict(img)[0].argmax())}
