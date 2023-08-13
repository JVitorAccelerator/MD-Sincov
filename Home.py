import streamlit as st

def main():
    with st.container():
        st.title("Perguntas relacionado ao SINCOV e análise da execução dos convênios")
        
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