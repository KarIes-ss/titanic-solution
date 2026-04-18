### Структура проекта

```
titanic-solution/
├── api/                # "Мозги" проекта
│   ├── main.py         # Код FastAPI
│   ├── model.cbm       # Ваша обученная модель
│   └── requirements.txt
├── frontend/           # Интерфейс
│   ├── app.py          # Код Streamlit
│   └── requirements.txt
├── notebooks/          # История ваших исследований
│   └── training.ipynb  # Тот самый колаб
├── docker-compose.yml  # Магия запуска одной командой
└── README.md           # Описание для судей
```