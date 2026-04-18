import streamlit as st
import requests

API_URL = st.secrets.get("API_URL", "http://127.0.0.1:8000/predict")

# 🔹 Настройки страницы
st.set_page_config(
    page_title="Titanic Predictor",
    page_icon="🚢",
    layout="centered"
)

st.title("Titanic Survival Predictor")

st.write("Введите данные пассажира и узнайте шанс выживания")

# 🔹 Форма (лучше, чем просто кнопки)
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

# 🔹 Логика
if submit:
    data = {
        "Pclass": pclass,
        "Sex": sex,
        "Age": age,
        "SibSp": sibsp,
        "Parch": parch,
        "Fare": fare,
        "Embarked": embarked
    }

    try:
        with st.spinner("Модель думает..."):
            response = requests.post(
                API_URL,
                json=data,
                timeout=10
            )
            response.raise_for_status()

        result = response.json()

        prediction = result["prediction"]
        proba = result["survival_probability"]

        st.subheader("Результат")

        if prediction == 1:
            st.success("🟢 Пассажир ВЫЖИВЕТ")
        else:
            st.error("🔴 Пассажир НЕ выживет")

        st.metric("Вероятность выживания", f"{proba:.2f}")

    except Exception as e:
        st.error("Ошибка подключения к API")
        st.write(e)