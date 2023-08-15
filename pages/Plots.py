from Classes import dataframe
import streamlit as st
from Components import plot_funcs as PF
from Components import data_funcs as D_Functions


df_convenio = dataframe.Dados.dimconvenio
df_data = dataframe.Dados.dimdata
df_emenda = dataframe.Dados.dimemenda
df_localizacao = dataframe.Dados.dimlocalizacao
df_parlamentar = dataframe.Dados.dimparlamentar
df_propostas = dataframe.Dados.dimproposta
df_fato = dataframe.Dados.fatoexecucao



datasets = ['Convenio', 'Data', 'Emenda', 'Localizacao', 'Parlamentar', 'Propostas', 'Fato']
st.title('Visualizador de dimensões')
selected_dataset = st.selectbox('Selecione uma dimensão:', datasets)
D_Functions.show_dataset(selected_dataset)

st.title("Análise por ministérios")
st.sidebar.title("Opções de interatividade")
ministerios = df_propostas['DES_ORGAO'].unique()
sit_convenio = df_convenio['SIT_CONVENIO'].unique()
selected_ministerio = st.sidebar.selectbox('Ministério:', ministerios)
selected_sit_convenio = st.sidebar.selectbox('Situação do convênio',sit_convenio)
#PF.analise_2(selected_ministerio, selected_sit_convenio)



st.title('📈Analises dos dados Sincov')
PF.Analise_1(df_data,df_fato,df_propostas,df_localizacao)





