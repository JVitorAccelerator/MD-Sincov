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
df_dataYear = df_data[["keyData","data_id","mes_texto","ano_texto"]].copy() # copiando algumas colunas do dataframe para um novo
df_dataYear = df_dataYear.rename(columns={'keyData': 'datakey'}) # Renomeando nome de coluna para conseguir fazer o merge
df_fato = df_fato.astype({'valorGlobal':'int'}) # Trocando para tipo int
st.write(df_fato.shape) # Tamanho de linhas e colunas
result = pd.merge(df_dataYear, df_fato, how="inner", on=['datakey']) # Juntando tabelas com base na chave datakey
df1 = pd.DataFrame(result.groupby(by=['ano_texto'])['valorGlobal'].sum()) # Agrupando informações da tabela de ano e com a soma do valor global
df1.reset_index(inplace=True) # Removendo index para a coluna ano aparecer
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
