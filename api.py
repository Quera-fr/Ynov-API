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
import pickle
import pandas as pd


with open('model.pkl', 'rb') as f:
    model = pickle.load(f)



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


