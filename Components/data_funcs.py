import pandas as pd
import plotly_express as px
import streamlit as st
import streamlit as st
import pandas as pd
from Classes import dataframe

df_convenio = dataframe.Dados.dimconvenio
df_data = dataframe.Dados.dimdata
df_emenda = dataframe.Dados.dimemenda
df_localizacao = dataframe.Dados.dimlocalizacao
df_parlamentar = dataframe.Dados.dimparlamentar
df_propostas = dataframe.Dados.dimproposta
df_fato = dataframe.Dados.fatoexecucao


def show_dataset(dataset):
    if dataset == 'Convenio':
        st.write(df_convenio)
    elif dataset == 'Data':
        st.write(df_data)
    elif dataset == 'Emenda':
        st.write(df_emenda)
    elif dataset == 'Localizacao':
        st.write(df_localizacao)
    elif dataset == 'Parlamentar':
        st.write(df_parlamentar)
    elif dataset == 'Propostas':
        st.write(df_propostas)
    elif dataset == 'Fato':
        st.write(df_fato)

datasets = ['Convenio', 'Data', 'Emenda', 'Localizacao', 'Parlamentar', 'Propostas', 'Fato']

st.title('Visualizador de Datasets')
selected_dataset = st.selectbox('Selecione um dataset:', datasets)


show_dataset(selected_dataset)
