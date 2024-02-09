import streamlit as st

# Define o estilo CSS para centralizar o texto e aumentar o tamanho da fonte
estilo = """
    <style>
        .centrado {
            text-align: center;
            font-size: 24px;
        }
        .title {
            font-size: 100px;
            text-align: center;
            font-weight: bold;
        }
        .subtitle {
            font-size: 40px;
            color: #0500E4;
            text-align: center;
        }
        .button {
            display: flex;
        }
    </style>
"""

# Escreve o texto com o estilo definido
st.markdown(estilo, unsafe_allow_html=True)
st.markdown('<p class="title">CyberAgro</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Planejamento de Otimização de Entregas</p>', unsafe_allow_html=True)
