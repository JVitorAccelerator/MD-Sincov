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
            '<li class="content-size">Identificar quais os objetos adquiridos por município de um ministério e total investido ?</li><br>'\
            '<li class="content-size">Qual a situação de cada prestação de contas do convênio por ministério e estado?</li><br>'\
            '<li class="content-size">Qual o valor contratado x valor de repasse x o valor em conta de um município ?</li><br>'\
            '<li class="content-size">Quais os objetos comprados por ministério, filtrando por situação de convênio e pelo Estado?</li><br>'\
            '<li class="content-size">Qual o valor contratado investido nas naturezas jurídicas por ano?</li><br>'\
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
    
    def formato_valor(soma_valor_total):
        numero_formatado = locale.currency(soma_valor_total, grouping=True, symbol='R$')
        return numero_formatado
        
    df_dataYear = df_data[["keyData","data_id","mes_texto","ano_texto"]].copy() # copiando algumas colunas do dataframe para um novo
    df_dataYear = df_dataYear.rename(columns={'keyData': 'datakey'}) # Renomeando nome de coluna para conseguir fazer o merge
    df_fato = df_fato.astype({'valorGlobal':'int'}) # Trocando para tipo int
    #st.write(df_fato.shape) # Tamanho de linhas e colunas
    result = pd.merge(df_dataYear, df_fato, how="inner", on=['datakey']) # Juntando tabelas com base na chave datakey

    df_proposta_filter = df_propostas[['key','DES_ORGAO','NATUREZA_JURIDICA','SIT_PROPOSTA','OBJETO_PROPOSTA']]
    df_proposta_filter = df_proposta_filter.rename(columns={'key': 'propostakey'})
    result = pd.merge(df_proposta_filter, result, how="inner", on=['propostakey'])

    localizacao_filter = df_localizacao[['key','UF_PROPONENTE','MUNIC_PROPONENTE','NM_PROPONENTE']]
    localizacao_filter = localizacao_filter.rename(columns={'key': 'localizacaokey'})
    result = pd.merge(localizacao_filter, result, how="inner", on=['localizacaokey'])

    convenio_filter = df_convenio[['key','SIT_CONVENIO']]
    convenio_filter = convenio_filter.rename(columns={'key': 'conveniokey'})
    result = pd.merge(convenio_filter, result, how="inner", on=['conveniokey'])

    result['count'] = result.groupby(['ano_texto'])['OBJETO_PROPOSTA'].transform('count')
    df1 = pd.DataFrame(result.groupby(by=['ano_texto','DES_ORGAO','count'])['valorGlobal'].sum()) # Agrupando informações da tabela de ano e com a soma do valor global
    df1.reset_index(inplace=True) # Removendo index para a coluna ano aparecer
    
    st.subheader(f"Total de investido por natureza jurídica:")

    lista_ano = set(df1['ano_texto'].map(int).to_list())
    selecao_year = st.slider(
        label='Ano: ',
        min_value=min(lista_ano),
        max_value=max(lista_ano),
        key="0")
    
    df_comLocalizacao = pd.DataFrame(result.groupby(by=['ano_texto','DES_ORGAO','UF_PROPONENTE','NATUREZA_JURIDICA','count','Repasse','SaldoReman'])['valorGlobal'].sum())
    df_comLocalizacao.reset_index(inplace=True) 
    df_comLocalizacao = df_comLocalizacao[df_comLocalizacao['ano_texto'] == str(selecao_year)]
    df_localizacaoGroupby = pd.DataFrame(df_comLocalizacao.groupby(by=['NATUREZA_JURIDICA'])['valorGlobal'].sum())
    df_localizacaoGroupby.reset_index(inplace=True) 

    cols1,cols2,cols3,cols4 = st.columns(4)
    cols1.metric("Quantidade de propostas", df_comLocalizacao['count'].sum())
    cols1.progress(100)

    cols2.metric("Valor contratado (Global)", formato_valor(df_comLocalizacao['valorGlobal'].sum()))
    cols2.progress(100)

    cols3.metric("Valor liberado (Repasse)", formato_valor(df_comLocalizacao['Repasse'].sum()))
    cols3.progress(100)

    cols4.metric("Saldo em conta", formato_valor(df_comLocalizacao['SaldoReman'].sum()))
    cols4.progress(100)

    fig_estados = px.bar(df_localizacaoGroupby, 
                x='NATUREZA_JURIDICA', 
                y='valorGlobal', 
                labels={
                        'NATUREZA_JURIDICA': 'Natureza jurídica',
                        'valorGlobal': 'Total'
                    },
                title=f"Análise de investimento contratado pela natureza jurídica no ano de {selecao_year}:",
                text='valorGlobal')
    #configura os textos para ficarem na parte de dentro das barras
    fig_estados.update_traces(textposition='inside',texttemplate='%{text:.2s}')
    #remove o eixo Y
    fig_estados.update_yaxes(showticklabels=False)
    st.write(fig_estados)

    st.subheader("Análise de objetos comprados pelos Ministérios")
    df_sit_convenio = pd.DataFrame(result.groupby(by=['ano_texto','DES_ORGAO','UF_PROPONENTE','MUNIC_PROPONENTE','OBJETO_PROPOSTA','SIT_CONVENIO'])['valorGlobal'].sum())
    df_sit_convenio.reset_index(inplace=True)
    df_sit_convenio = df_sit_convenio[df_sit_convenio['ano_texto'] == str(selecao_year)]
    st.markdown("##### Nesta análise estamos usando a situação do convênio e o Estado")
    selected_orgao = st.selectbox('Selecione o ministério:',set(df_sit_convenio['DES_ORGAO'].to_list()))
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
    
    st.subheader('Analises por ministérios')
    st.markdown("##### Análise por valor contratado de ministérios por estado e município")
    df_ministerio_por_ano_copy = result.copy()
    df_ministerio_por_ano_copy['qtdSitConvenio'] = df_ministerio_por_ano_copy.groupby(['ano_texto','DES_ORGAO','UF_PROPONENTE'])['SIT_CONVENIO'].transform('count')
    coluna1, coluna2 = st.columns([3,1])
    with coluna1:
        select_orgao = st.selectbox('Ministério:',set(df_ministerio_por_ano_copy['DES_ORGAO'].to_list()))
        df_ministerio_por_ano_copy = filter_df(df_ministerio_por_ano_copy,'DES_ORGAO',select_orgao)
    with coluna2:
        selecao_estado = st.selectbox('Selecione a UF:',set(df_ministerio_por_ano_copy['UF_PROPONENTE'].to_list()))
        df_ministerio_por_ano = filter_df(df_ministerio_por_ano_copy,'UF_PROPONENTE',selecao_estado)
    df1_filtro = pd.DataFrame(df_ministerio_por_ano.groupby(by=['ano_texto'])['valorGlobal'].sum())
    df1_filtro.reset_index(inplace=True)

    fig_year = px.bar(df1_filtro, x='ano_texto', y='valorGlobal', labels={'ano_texto': 'Ano','valorGlobal': 'Total'})
    st.write(fig_year)

    fig_pie = px.pie(df_ministerio_por_ano, values='qtdSitConvenio', names='SIT_CONVENIO', color='ano_texto',title='Situação de prestação de contas do Convênio por Ministério e Estado',hole=.3,labels={'qtdSitConvenio':'Quantidade','SIT_CONVENIO':'Situação do convênio','ano_texto':'Ano'})
    st.write(fig_pie)


    if select_orgao == None:
        st.write('⚠️ Selecione um orgão acima ⚠️')
    else:
        df_ministerio_por_ano_filtro = df_ministerio_por_ano.copy()
        st.markdown(f"##### Análise de investimentos nos municípios do(a) {selecao_estado}")
        colun1, colun2 = st.columns([1,3])
        with colun1:
            selecao_ano = st.selectbox('Selecione o Ano:',set(df_ministerio_por_ano_filtro['ano_texto'].to_list()))
            df_ministerio_por_ano_filtro = filter_df(df_ministerio_por_ano_filtro,'ano_texto',selecao_ano)
            nome_uf = df_ministerio_por_ano_filtro['UF_PROPONENTE'].iloc[0]
            valor_total = df_ministerio_por_ano_filtro['valorGlobal'].sum()
            colun1.metric(label="Valor contratado (Global)", value=formato_valor(valor_total))
            colun1.progress(100)
            colun1.metric(label="Valor liberado (Repasse)", value=formato_valor(df_ministerio_por_ano_filtro['Repasse'].sum()))
            colun1.progress(100)
            colun1.metric(label="Saldo em conta", value=formato_valor(df_ministerio_por_ano_filtro['SaldoReman'].sum()))
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