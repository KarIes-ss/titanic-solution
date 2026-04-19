# Titanic Survival Predictor

ML модель для предсказания вероятности выживания пассажиров Титаника.

[Live Demo](https://titanic-solution-main.streamlit.app/) | [API](https://titanic-solution.onrender.com) | [Notebook](notebooks/titanic.ipynb)

## О проекте

Веб-приложение предсказывает шанс выживания пассажира на основе его характеристик.

**Accuracy:** 82%

## Архитектура

```
Streamlit Frontend (Streamlit Cloud)
         |
         | POST /predict
         v
FastAPI Backend (Render) + CatBoost Model
```

## Быстрый старт

```bash
git clone <repo>
cd titanic-solution
pip install -r requirements.txt

# Terminal 1: API
uvicorn api.main:app --reload

# Terminal 2: Frontend
streamlit run frontend/app.py
```

## Tech Stack

- **Model:** CatBoost
- **Backend:** FastAPI + Uvicorn
- **Frontend:** Streamlit
- **Deployment:** Render + Streamlit Cloud
- **Data:** Pandas, NumPy, Scikit-learn

## Структура

```
├── api/                    # FastAPI endpoints
├── frontend/               # Streamlit interface
├── notebooks/              # EDA + training
│   ├── titanic.ipynb
│   ├── cat_model.cbm
│   └── titanic_dataset/
└── requirements.txt
```

## Deploy

### Render (API)
```bash
uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

### Streamlit Cloud (Frontend)
- App file: `frontend/app.py`
- Secrets: `API_URL = https://titanic-solution.onrender.com/predict`

## Признаки

- Pclass (1-3)
- Sex (male/female)
- SibSp
- Parch
- Age
- Fare
- Embarked (S/C/Q)

## Что сделано

- Обучение на 891 samples
- Cross-validation и hyperparameter tuning
- Сравнение моделей (RandomForest, XGBoost, CatBoost)
- Deployment на облачных сервисах
- REST API для интеграции

