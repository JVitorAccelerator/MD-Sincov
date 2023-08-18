from Classes import dataframe
import streamlit as st
#from Components import data_funcs as D_Functions
import pandas as pd
import plotly_express as px
import plotly.graph_objects as go
import locale

def main():
    
    with st.container():
        st.title("Perguntas relacionado ao siconv e análise da execução dos convênios")
        
        st.write("")

    with st.container():

        
        st.header('Perguntas')

        st.write("")


        objectives =(


            '<ul>' \
            '<li class="content-size">As propostas gastaram mais ou menos na execução dos convênios?</li><br>'\
            '<li class="content-size">Existe alguma relação entre o tamanho do repasse das propostas e o valor gasto na execução dos convênios?</li><br>'\
            '<li class="content-size"> Quais são os principais tipos de projetos que receberam convênios e como eles se comparam em termos de repasses e gastos?</li><br>'\
            '<li class="content-size"> "Qual é a tendência ao longo do tempo em relação ao valor médio de repasse e gastos em convênios?</li><br>'\
            '</ul>'



            """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """    
        )


        st.markdown(objectives, unsafe_allow_html=True)


main()






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



def Analise_1(df_data,df_fato,df_propostas,df_localizacao,df_convenio):

    def filter_df(df, column_name, value):
        filter_sales_units = df[(df[column_name] == value)]
        return filter_sales_units
    
    def formato_real(valor):
        return f'R${valor:.2f}'.replace('.', ',')
        
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

    convenio_filter = df_convenio[['key','SIT_CONVENIO']]
    convenio_filter = convenio_filter.rename(columns={'key': 'conveniokey'})
    result = pd.merge(convenio_filter, result, how="inner", on=['conveniokey'])

    result['count'] = result.groupby(['ano_texto','DES_ORGAO'])['OBJETO_PROPOSTA'].transform('count')
    df1 = pd.DataFrame(result.groupby(by=['ano_texto','DES_ORGAO','count'])['valorGlobal'].sum()) # Agrupando informações da tabela de ano e com a soma do valor global
    df1.reset_index(inplace=True) # Removendo index para a coluna ano aparecer

    lista_ano = set(df1['ano_texto'].map(int).to_list())
    with st.expander('Filtros'):
        selecao_year = st.slider(
            label='Ano: ',
            min_value=min(lista_ano),
            max_value=max(lista_ano),
            key="0")
        filtro = filter_df(df1,'ano_texto',str(selecao_year))
        multiselect_orgao = st.multiselect(
            label='Orgão:',
            options=filtro['DES_ORGAO'].to_list(),
            default=['MINISTERIO DA DEFESA'],
            key="1")
        filtro = filtro[filtro["DES_ORGAO"].isin(multiselect_orgao)]
    lista_orgao_filtrada = filtro['DES_ORGAO'].to_list()
    lista_qtd_propostas = filtro['count'].to_list()
    st.subheader(f"Quantidade de prpostas no ano de {selecao_year} ?")
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

    st.subheader(f"Total investido por estado em {selecao_year}:")

    fig_estados = px.bar(df_localizacaoGroupby, 
                x='UF_PROPONENTE', 
                y='valorGlobal', 
                labels={
                        'UF_PROPONENTE': 'Estado',
                        'valorGlobal': 'Total'
                    },
                title=f"Total de investido por orgão em {selecao_year}:",
                text='valorGlobal')
    #configura os textos para ficarem na parte de dentro das barras
    fig_estados.update_traces(textposition='inside',texttemplate='%{text:.2s}')
    #remove o eixo Y
    fig_estados.update_yaxes(showticklabels=False)
    st.write(fig_estados)

    st.subheader("Análise de objetos comprados pelos Orgãos")
    df_sit_convenio = pd.DataFrame(result.groupby(by=['ano_texto','DES_ORGAO','UF_PROPONENTE','MUNIC_PROPONENTE','OBJETO_PROPOSTA','SIT_CONVENIO'])['valorGlobal'].sum())
    df_sit_convenio.reset_index(inplace=True)
    df_sit_convenio = df_sit_convenio[df_sit_convenio['ano_texto'] == str(selecao_year)]
    st.markdown("##### Nesta análise estamos usando a situação do convênio e o Estado")
    selected_orgao = st.selectbox('Selecione o orgao:',set(df_sit_convenio['DES_ORGAO'].to_list()))
    df_orgao_filtrado = filter_df(df_sit_convenio,'DES_ORGAO',selected_orgao)
    col_convenio, col_uf = st.columns(2)
    with col_convenio:
        selected_sit_convenio = st.selectbox('Selecione a situação do convênio:',set(df_orgao_filtrado['SIT_CONVENIO'].to_list()))
    df_sit_convenio_filtrado = filter_df(df_sit_convenio,'SIT_CONVENIO',selected_sit_convenio)
    with col_uf:
        selected_uf = st.selectbox('Selecione a UF:',set(df_sit_convenio_filtrado['UF_PROPONENTE'].to_list()))
    df_sit_convenio_filtrado2 = filter_df(df_sit_convenio_filtrado,'UF_PROPONENTE',selected_uf)
    df_sit_convenio_filtrado2['valor_formatado'] = df_sit_convenio_filtrado2['valorGlobal'].apply(formato_real)
    table = go.Figure(data=[go.Table(header=dict(values=['Objetos', 'Municipio','Valor'],line_color='darkslategray',fill_color='royalblue', font=dict(color='white', size=12),),
                 cells=dict(values=[df_sit_convenio_filtrado2['OBJETO_PROPOSTA'], df_sit_convenio_filtrado2['MUNIC_PROPONENTE'],df_sit_convenio_filtrado2['valor_formatado']],line_color='darkslategray'))
                     ])
    st.write(table)
    

    st.title('Analises Subplots')
    st.markdown("### Análise por ministério ao passar dos anos")
    df_ministerio_por_ano_copy = result.copy()
    coluna1, coluna2 = st.columns([3,1])
    with coluna1:
        multiselect_orgao = st.multiselect('Orgão:',set(df_ministerio_por_ano_copy['DES_ORGAO'].to_list()),['MINISTERIO DA DEFESA'])
        df_ministerio_por_ano_copy = df_ministerio_por_ano_copy[df_ministerio_por_ano_copy["DES_ORGAO"].isin(multiselect_orgao)]
    with coluna2:
        selecao_estado = st.selectbox('Selecione a UF:',set(df_ministerio_por_ano_copy['UF_PROPONENTE'].to_list()))
        df_ministerio_por_ano = filter_df(df_ministerio_por_ano_copy,'UF_PROPONENTE',selecao_estado)
    df1_filtro = pd.DataFrame(df_ministerio_por_ano.groupby(by=['ano_texto'])['valorGlobal'].sum())
    df1_filtro.reset_index(inplace=True)

    fig_year = px.bar(df1_filtro, x='ano_texto', y='valorGlobal', labels={'ano_texto': 'Ano','valorGlobal': 'Total'})
    st.write(fig_year)

    if multiselect_orgao == []:
        st.write('⚠️ Selecione um orgão acima ⚠️')
    else:
        st.markdown("### Análise de investimentos nos municípios por estado ")
        df_ministerio_por_ano_filtro = df_ministerio_por_ano.copy()
        colun1, colun2 = st.columns([1,3])
        with colun1:
            selecao_ano = st.selectbox('Selecione o Ano:',set(df_ministerio_por_ano_filtro['ano_texto'].to_list()))
            df_ministerio_por_ano_filtro = filter_df(df_ministerio_por_ano_filtro,'ano_texto',selecao_ano)
            nome_uf = df_ministerio_por_ano_filtro['UF_PROPONENTE'].iloc[0]
            soma_valor_total = df_ministerio_por_ano_filtro['valorGlobal'].sum()
            numero_formatado = locale.currency(soma_valor_total, grouping=True, symbol='R$')
            colun1.metric(label=f"Estado de {nome_uf}", value=numero_formatado)
            colun1.progress(100)

        df_teste_filtro = pd.DataFrame(df_ministerio_por_ano_filtro.groupby(by=['ano_texto','MUNIC_PROPONENTE','count'])['valorGlobal'].sum()) # Agrupando informações da tabela de ano e com a soma do valor global
        df_teste_filtro.reset_index(inplace=True)
        with colun2:
            figura = px.bar(df_teste_filtro, x='MUNIC_PROPONENTE', y='valorGlobal',labels={'MUNIC_PROPONENTE': 'Municipio','valorGlobal': 'Total'})
            st.write(figura)

with open ('./css/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

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
show_dataset(selected_dataset)

st.title('📈Analises dos dados siconv')
Analise_1(df_data,df_fato,df_propostas,df_localizacao,df_convenio)



def Analise_2(df_data,df_fato,df_propostas,df_localizacao,df_convenio):
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

    convenio_filter = df_convenio[['key','SIT_CONVENIO']]
    convenio_filter = convenio_filter.rename(columns={'key': 'conveniokey'})
    result = pd.merge(convenio_filter, result, how="inner", on=['conveniokey'])

    result['count'] = result.groupby(['ano_texto','DES_ORGAO'])['OBJETO_PROPOSTA'].transform('count')
    df1 = pd.DataFrame(result.groupby(by=['ano_texto','DES_ORGAO','count'])['valorGlobal'].sum()) # Agrupando informações da tabela de ano e com a soma do valor global
    df1.reset_index(inplace=True) # Removendo index para a coluna ano aparecer


    lista_ano = set(df1['ano_texto'].map(int).to_list())
    
    with st.expander('Filtros'):
        selecao_year = st.slider(
            label='Ano: ',
            min_value=min(lista_ano),
            max_value=max(lista_ano),
            key="2")
        filtro = filter_df(df1,'ano_texto',str(selecao_year))
        multiselect_orgao = st.multiselect(
            label='Orgão:',
            options=filtro['DES_ORGAO'].to_list(),
            default=['MINISTERIO DA DEFESA'],
            key="3")
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

    fig_estados = px.bar(df_localizacaoGroupby, 
                x='UF_PROPONENTE', 
                y='valorGlobal', 
                labels={
                        'UF_PROPONENTE': 'Estado',
                        'valorGlobal': 'Total'
                    },
                title=f"Total de investido por orgão em {selecao_year}",
                text='valorGlobal')
    #configura os textos para ficarem na parte de dentro das barras
    fig_estados.update_traces(textposition='inside',texttemplate='%{text:.2s}')
    #remove o eixo Y
    fig_estados.update_yaxes(showticklabels=False)
    st.write(fig_estados)


    #Adiciona filtro de estados, e criar um gráfico com a quantidade de situações dos convênios


    st.title("Análise por ministérios")
    df_sit_convenio = pd.DataFrame(result.groupby(by=['ano_texto','DES_ORGAO','UF_PROPONENTE','MUNIC_PROPONENTE','OBJETO_PROPOSTA','SIT_CONVENIO'])['valorGlobal'].sum())
    df_sit_convenio.reset_index(inplace=True)
    df_sit_convenio = df_sit_convenio[df_sit_convenio['ano_texto'] == str(selecao_year)]
    st.markdown("##### Nesta análise estamos usando a situação do convênio e o Estado")
    selected_orgao = st.selectbox(
        label='Selecione o orgao:',
        options=set(df_sit_convenio['DES_ORGAO'].to_list()),
        key="4")
    df_orgao_filtrado = filter_df(df_sit_convenio,'DES_ORGAO',selected_orgao)
    col_convenio, col_uf = st.columns(2)
    with col_convenio:
        selected_sit_convenio = st.selectbox(
            label='Selecione a situação do convênio:',
            options=set(df_orgao_filtrado['SIT_CONVENIO'].to_list()),
            key="5")
    df_sit_convenio_filtrado = filter_df(df_sit_convenio,'SIT_CONVENIO',selected_sit_convenio)
    with col_uf:
        selected_uf = st.selectbox(
            label='Selecione a UF:',
            options=set(df_sit_convenio_filtrado['UF_PROPONENTE'].to_list()),
            key="6")
    df_sit_convenio_filtrado2 = filter_df(df_sit_convenio_filtrado,'UF_PROPONENTE',selected_uf)
    st.write(df_sit_convenio_filtrado2[['MUNIC_PROPONENTE','OBJETO_PROPOSTA','valorGlobal']])

#Analise_2(df_data,df_fato,df_propostas,df_localizacao,df_convenio)








