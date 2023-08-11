from Classes import dataframe
import streamlit as st
import pandas as pd
import plotly_express as px

df_convenio = dataframe.Dados.dimconvenio
df_data = dataframe.Dados.dimdata
df_emenda = dataframe.Dados.dimemenda
df_localizacao = dataframe.Dados.dimlocalizacao
df_parlamentar = dataframe.Dados.dimparlamentar
df_propostas = dataframe.Dados.dimproposta
df_fato = dataframe.Dados.fatoexecucao


#  ----- Gráfico de Total insvestido por ano ------
df_dataYear = df_data[["keyData","data_id","mes_texto","ano_texto"]].copy()
df_dataYear = df_dataYear.rename(columns={'keyData': 'datakey'})
df_fato = df_fato.astype({'valorGlobal':'int'})
result = pd.merge(df_dataYear, df_fato, how="inner", on=['datakey'])
df1 = pd.DataFrame(result.groupby(by=['ano_texto'])['valorGlobal'].sum())
df1.reset_index(inplace=True)
st.table(df1)
fig = px.bar(df1, 
             x='ano_texto', 
             y='valorGlobal', 
             labels={
                     'ano_texto': 'Ano',
                     'valorGlobal': 'Valor total'
                },
             title="Total de investido por ano")
st.write(fig)
