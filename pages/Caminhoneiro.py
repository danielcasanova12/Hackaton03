import time
import streamlit as st
import pandas as pd
import pydeck as pdk
import json
import requests
from googletrans import Translator
import subprocess
import math
from datetime import datetime, timedelta

st.set_page_config(page_title="CyberAgro", page_icon=":bar_chart:", layout="wide")

# Inicialize o tradutor
translator = Translator()

API_KEY='d1c582f009b19572310e488e97ec78ae'
city = "Cascavel"
link=f"https://api.openweathermap.org/data/2.5/weather?lat={-24.9573}&lon={-53.4590}&appid={API_KEY}"

requisicao = requests.get(link)
requisicao_json = requisicao.json()
descricao_ingles = requisicao_json['weather'][0]['description']

def kelvin_to_celsius(kelvin):
    celsius = kelvin - 273.15
    return celsius

temperatura= requisicao_json['main']['temp_max']
temperatura = kelvin_to_celsius(temperatura)
st.write(f"A temperatura atual é: {temperatura:.2f}°C")

# Descrição do clima em inglês
descricao_ingles = requisicao_json['weather'][0]['description']

# Traduza para o português
descricao_portugues = translator.translate(descricao_ingles, src='en', dest='pt').text

# Exiba a descrição do clima com estilo
st.write(f"Previsão do tempo: {descricao_portugues}")
cidades = [
    {
        "name": "Carlos - Antonio- marcos",
        "color": "#ed1c24",
        "path": [
            [-53.380980, -24.979704],
            [-53.371836, -24.984359],[-53.369948,-24.984710 ],
            [-53.369304,-24.985137 ],[-53.373209,-24.988755 ],[-53.372270, -24.991118],
            
        ],
        "concluida": False 
    },
    {
        "name": "Carlos - Antonio- marcos",
        "color": "#faa61a",
        "path": [
            [-53.372270, -24.991118],
            [-53.377447, -24.994784],
            [-53.375236, -24.996787]
        ],
        "concluida": False 
    },
    {
        "name": "Carlos - Antonio- marcos",
        "color": "#ffe800",
        "path": [
            [-53.375236, -24.996787],
            [-53.375236,-24.996787],
            [ -53.371159,-24.994520],
            [-53.368615,-24.997170],
            [-53.366674,-25.003405],
            [-53.368434,-25.008262],
            [-53.366725,-25.010806],
            [-53.363203,-25.010690],
            [-53.359937,-25.012355],
            [-53.359937,-25.012355],
            [-53.358278,-25.011731],
             ]
    },
    {
        "name": "Felipe - Daniel",
        "color": "#00aeef",
        "path": [
            [-53.380980, -24.979704],
            [-53.386557, -24.976543],
            [-53.394899, -24.971243],
            [-53.390549, -24.964779]
        ]
    },
    {
        "name": "Felipe - Daniel",
        "color": "#4db848",
        "path": [
[-53.392764, -24.967991],
[-53.394142, -24.965053],
        ]
    }
]


cidades_json = json.dumps(cidades, indent=2)
  


DATA_URL = cidades_json
df = pd.read_json(DATA_URL)


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


df["color"] = df["color"].apply(hex_to_rgb)

    # Selecionando as rotas
df1 = df


selected_route = st.selectbox("Selecione a rota", df["name"].unique())

df_selected = df[df["name"] == selected_route]

selected_route_name = selected_route
def get_current_datetime():
    return datetime.now()

# Função para calcular a hora final com base na hora atual e na duração da rota
def calculate_end_time(start_time, duration):
    end_time = start_time + timedelta(minutes=duration)  # Supondo que a duração seja em minutos
    return end_time

hora_inicio = get_current_datetime()
data_atual = datetime.now().date()
hora_fim = 14
tempo_total = 2


# Salva o nome da rota em um arquivo de texto chamado 'api.txt'

def start_timer(duration):
    start_time = time.time()
    elapsed_time = 0

    while elapsed_time < duration:
        elapsed_time = time.time() - start_time
        remaining_time = duration - elapsed_time
        remaining_time_rounded = math.ceil(remaining_time)  
        st.write(f"Inicio da rota em   {remaining_time_rounded} segundos")
        time.sleep(1)  

    st.write("Rora Iniciada")

# Variável para controlar se o temporizador está em execução
timer_running = False

if st.button("Começar Rota", key="start_button"):
    if not timer_running:
        duration = 5  # Defina a duração do temporizador em segundos
        timer_running = True
        start_timer(duration)
        with open("relatorio.txt", "a") as file:
            file.write(f"Data: {data_atual}\n")
            file.write(f"Hora de Início: {hora_inicio}\n")
            file.write(f"Hora de Fim: {hora_fim}\n")
            file.write(f"Tempo Total: {tempo_total}\n")
            file.write(f"Rota: {selected_route_name}\n\n")
        with open("./api.txt", "w") as file:
            file.write(selected_route_name)    

    else:
        st.write("Temporizador já está em execução!")


    # Renderize o seletor de rotas e o DataFrame selecionado apenas se a rota não foi concluída
    # if selected_route is None:
    #     selected_route = st.selectbox("Selecione a rota", df["name"].unique())

        # Atualize df_selected com base na rota selecionada
        # df_selected = df[df["name"] == selected_route]

    # # Renderize o DataFrame selecionado
    # if df_selected is not None:
    #     st.write("Rota Selecionada:", selected_route)
    #     st.write(df_selected)

    




view_state = pdk.ViewState(latitude=-25.0107224, longitude=-53.3952989, zoom=10)

layer = pdk.Layer(
    type="PathLayer",
    data=df_selected,
    pickable=True,
    get_color="color",
    width_scale=20,
    width_min_pixels=2,
    get_path="path",
    get_width=5,
)
    

# st.sidebar.title('CyberAgro')
# st.sidebar.write("Menu")




# Renderizando no Streamlit
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))    
