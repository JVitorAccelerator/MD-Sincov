import pandas as pd
import plotly_express as px
import streamlit as st

def Analise_1(df_data,df_fato,df_propostas,df_localizacao):

    def filter_df(df, column_name, value):
        filter_sales_units = df[(df[column_name] == value)]
        return filter_sales_units
    
    df_dataYear = df_data[["keyData","data_id","mes_texto","ano_texto"]].copy() # copiando algumas colunas do dataframe para um novo
    df_dataYear = df_dataYear.rename(columns={'keyData': 'datakey'}) # Renomeando nome de coluna para conseguir fazer o merge
    df_fato = df_fato.astype({'valorGlobal':'int'}) # Trocando para tipo int
    #st.write(df_fato.shape) # Tamanho de linhas e colunas
    result = pd.merge(df_dataYear, df_fato, how="inner", on=['datakey']) # Juntando tabelas com base na chave datakey

    df_proposta_filter = df_propostas[['key','DES_ORGAO','SIT_PROPOSTA','OBJETO_PROPOSTA']]
    df_proposta_filter = df_proposta_filter.rename(columns={'key': 'propostakey'})
    result = pd.merge(df_proposta_filter, result, how="inner", on=['propostakey'])

    localizacao_filter = df_localizacao[['key','UF_PROPONENTE','MUNIC_PROPONENTE','NM_PROPONENTE']]
    localizacao_filter = localizacao_filter.rename(columns={'key': 'localizacaokey'})
    result = pd.merge(localizacao_filter, result, how="inner", on=['localizacaokey'])
    result['count'] = result.groupby(['ano_texto','DES_ORGAO'])['OBJETO_PROPOSTA'].transform('count')
    df1 = pd.DataFrame(result.groupby(by=['ano_texto','DES_ORGAO','count'])['valorGlobal'].sum()) # Agrupando informações da tabela de ano e com a soma do valor global
    df1.reset_index(inplace=True) # Removendo index para a coluna ano aparecer

    lista_ano = set(df1['ano_texto'].map(int).to_list())
    with st.expander('Filtros'):
        selecao_year = st.slider('Ano: ',min_value=min(lista_ano),max_value=max(lista_ano))
        filtro = filter_df(df1,'ano_texto',str(selecao_year))
        multiselect_orgao = st.multiselect('Orgão:',filtro['DES_ORGAO'].to_list())
        filtro = filtro[filtro["DES_ORGAO"].isin(multiselect_orgao)]
    lista_orgao_filtrada = filtro['DES_ORGAO'].to_list()
    lista_qtd_propostas = filtro['count'].to_list()
    st.subheader(f"Quais as propostas e a quantidade para o ano de {selecao_year} ?")
    # Definir quantas colunas por grupo você quer
    colunas_por_grupo = 3
    # Calcular o número total de grupos
    num_grupos = (len(lista_orgao_filtrada) + colunas_por_grupo - 1) // colunas_por_grupo
    # Criar os grupos de colunas e simular a quebra de linha
    cont = 0
    for grupo_num in range(num_grupos):
        inicio = grupo_num * colunas_por_grupo
        fim = min((grupo_num + 1) * colunas_por_grupo, len(lista_orgao_filtrada))
        grupo_orgaos = lista_orgao_filtrada[inicio:fim]
        # Criar um grupo de colunas para este conjunto de órgãos
        with st.container():
            cols = st.columns(len(grupo_orgaos))
            for index, orgao in enumerate(grupo_orgaos):
                col = cols[index]
                col.metric(orgao, lista_qtd_propostas[cont])
                col.progress(100)
                cont+=1

    df_comLocalizacao = pd.DataFrame(result.groupby(by=['ano_texto','DES_ORGAO','UF_PROPONENTE'])['valorGlobal'].sum())
    df_comLocalizacao.reset_index(inplace=True) 
    df_comLocalizacao = df_comLocalizacao[df_comLocalizacao['ano_texto'] == str(selecao_year)]
    df_comLocalizacao = df_comLocalizacao[df_comLocalizacao['DES_ORGAO'].isin(multiselect_orgao)]
    df_localizacaoGroupby = pd.DataFrame(df_comLocalizacao.groupby(by=['UF_PROPONENTE'])['valorGlobal'].sum())
    df_localizacaoGroupby.reset_index(inplace=True) 

    st.subheader(f"Quais os estados com maiores investimentos em {selecao_year} ?")

    fig = px.bar(df_localizacaoGroupby, 
                x='UF_PROPONENTE', 
                y='valorGlobal', 
                labels={
                        'UF_PROPONENTE': 'Estado',
                        'valorGlobal': 'Valor total'
                    },
                title=f"Total de investido por orgão em {selecao_year}",
                text_auto=True)
    st.write(fig)



