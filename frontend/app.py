import streamlit as st
import pandas as pd
from pathlib import Path
from catboost import CatBoostClassifier

MODEL_PATH = Path(__file__).resolve().parent.parent / "notebooks" / "cat_model.cbm"

@st.cache_resource
def load_model():
    model = CatBoostClassifier()
    model.load_model(str(MODEL_PATH), format="cbm")
    return model

model = load_model()

# 🔹 Настройки страницы
st.set_page_config(
    page_title="Titanic Predictor",
    page_icon="🚢",
    layout="centered"
)

st.title("Titanic Survival Predictor")

st.write("Введите данные пассажира и узнайте шанс выживания")

# 🔹 Форма
with st.form("prediction_form"):

    col1, col2 = st.columns(2)

    with col1:
        pclass = st.selectbox("Pclass", [1, 2, 3])
        sex = st.selectbox("Sex", ["male", "female"])
        age = st.slider("Age", 0, 80, 25)

    with col2:
        sibsp = st.number_input("SibSp", 0, 10, 0)
        parch = st.number_input("Parch", 0, 10, 0)
        fare = st.number_input("Fare", 0.0, 500.0, 10.0)

    embarked = st.selectbox("Embarked", ["S", "C", "Q"])

    submit = st.form_submit_button("Predict")

# 🔹 Логика предсказания
if submit:
    data = pd.DataFrame([{
        "Pclass": pclass,
        "Sex": sex,
        "SibSp": sibsp,
        "Parch": parch
    }])

    data = pd.get_dummies(data, columns=["Sex"], drop_first=False)
    for col in ["Sex_female", "Sex_male"]:
        if col not in data.columns:
            data[col] = 0
    data = data[["Pclass", "SibSp", "Parch", "Sex_female", "Sex_male"]]

    with st.spinner("Модель думает..."):
        prediction = int(model.predict(data)[0])
        proba = float(model.predict_proba(data)[0][1])

    st.subheader("Результат")
    if prediction == 1:
        st.success("🟢 Пассажир ВЫЖИВЕТ")
    else:
        st.error("🔴 Пассажир НЕ выживет")

    st.metric("Вероятность выживания", f"{proba:.2f}")