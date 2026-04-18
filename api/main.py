import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from catboost import CatBoostClassifier
from pathlib import Path

app = FastAPI()

MODEL_PATH = Path(__file__).resolve().parent.parent / "notebooks" / "cat_model.cbm"
cat_model = CatBoostClassifier()
cat_model.load_model(str(MODEL_PATH), "cbm")

class Passenger(BaseModel):
    Pclass: int
    Sex: str          # "male" / "female"
    Age: float | None = None
    SibSp: int
    Parch: int
    Fare: float
    Embarked: str     # "S", "C", "Q"

@app.get("/")
def root():
    return {"message": "Titanic API is running"}

@app.post("/predict")
def predict(passenger: Passenger):
    # Берем только те колонки, на которых обучалась модель
    data = pd.DataFrame([{
        "Pclass": passenger.Pclass,
        "Sex": passenger.Sex,
        "SibSp": passenger.SibSp,
        "Parch": passenger.Parch
    }])
    
    # Применяем get_dummies с явным указанием категорий
    data = pd.get_dummies(data, columns=["Sex"], drop_first=False)
    
    # Убедимся, что все ожидаемые колонки присутствуют в правильном порядке
    expected_cols = ["Pclass", "SibSp", "Parch", "Sex_female", "Sex_male"]
    for col in expected_cols:
        if col not in data.columns:
            data[col] = 0
    
    # Выбираем только нужные колонки в правильном порядке
    data = data[expected_cols]

    # Предсказание
    pred = cat_model.predict(data)[0]
    proba = cat_model.predict_proba(data)[0][1]
    
    return {
        "prediction": int(pred),
        "survival_probability": float(proba)
    }