from Classes import dataframe
import streamlit as st
from Components import plot_funcs as PF
from Components import data_funcs as dataF


df_convenio = dataframe.Dados.dimconvenio
df_data = dataframe.Dados.dimdata
df_emenda = dataframe.Dados.dimemenda
df_localizacao = dataframe.Dados.dimlocalizacao
df_parlamentar = dataframe.Dados.dimparlamentar
df_propostas = dataframe.Dados.dimproposta
df_fato = dataframe.Dados.fatoexecucao





st.title('📈Analises dos dados Sincov')
PF.Analise_1(df_data,df_fato,df_propostas,df_localizacao)



dataF.show_dataset()

