import streamlit as st
import pandas as pd

# Carregar os dados das rotas do caminhoneiro
def load_data_from_file():
    with open("relatorio.txt", "r") as file:
        lines = file.readlines()

    data = {
        "Data": [line.split(": ")[1].strip() for line in lines if line.startswith("Data")],
        "Hora Início": [line.split(": ")[1].strip() for line in lines if line.startswith("Hora de Início")],
        "Hora Fim": [line.split(": ")[1].strip() for line in lines if line.startswith("Hora de Fim")],
        "Tempo Total": [line.split(": ")[1].strip() for line in lines if line.startswith("Tempo Total")],
        "Rota": [line.split(": ")[1].strip() for line in lines if line.startswith("Rota")]
    }
    df = pd.DataFrame(data)
    return df


# Função para calcular o tempo total de trabalho
def calculate_total_time(df):
    total_time = pd.to_timedelta(df["Tempo Total"]).sum()
    return total_time

# Carregar os dados das rotas do caminhoneiro
df = load_data_from_file()

# Calcular o tempo total de trabalho
total_time = calculate_total_time(df)

# Renderizar a tela de relatórios
st.title("Relatórios do Motorista01")

st.subheader("Rotas do Dia")
st.write(df)
