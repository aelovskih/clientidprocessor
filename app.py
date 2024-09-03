import streamlit as st
import pandas as pd
import re


# Функция для извлечения названия клиента из поля Summary
def extract_client_name(summary):
    return summary.split('::')[0].strip() if '::' in summary else summary


# Функция для извлечения clientID из поля Description с более гибким регулярным выражением
def search_flexible_client_id(description):
    if pd.isna(description):
        return "clientID отсутствует"
    match = re.search(r'\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\s*(\d+\.\d+)', description)
    if match:
        return match.group(1)
    return "clientID отсутствует"


# Заголовок приложения
st.title("JIRA clientID Processor")

# Загрузка файла
uploaded_file = st.file_uploader("Загрузите CSV файл", type="csv")

if uploaded_file is not None:
    # Чтение данных из загруженного файла
    data = pd.read_csv(uploaded_file)

    # Проверяем, содержатся ли в файле необходимые столбцы
    required_columns = ['Summary', 'Issue key', 'Description', 'Status']
    if all(column in data.columns for column in required_columns):

        # Обработка данных
        data['Client Name'] = data['Summary'].apply(extract_client_name)
        data['ClientID'] = data['Description'].apply(search_flexible_client_id)

        # Убираем лишние столбцы и фильтруем строки
        final_data = data[['Client Name', 'Issue key', 'Status', 'ClientID']]
        filtered_data = final_data[final_data['ClientID'] != "clientID отсутствует"]

        # Отображаем таблицу
        st.write("Обработанные данные:")
        st.dataframe(filtered_data)

        # Предлагаем скачать обработанный файл
        csv = filtered_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Скачать обработанный CSV",
            data=csv,
            file_name='filtered_simplified_agima_jira.csv',
            mime='text/csv',
        )
    else:
        st.error("Файл не содержит необходимых столбцов.")
