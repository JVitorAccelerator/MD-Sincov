import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


data_dimension_df = pd.read_csv('C:\Users\kazef\Desktop\SINCOV-Streamlit\MD-Sincov\Data\dimdata.csv')
localization_dimension_df = pd.read_csv('C:\Users\kazef\Desktop\SINCOV-Streamlit\MD-Sincov\Data\dimlocalizacao.csv')
proposta_dimension_df = pd.read_csv('C:\Users\kazef\Desktop\SINCOV-Streamlit\MD-Sincov\Data\dimproposta.csv')
parlamentar_dimension_df = pd.read_csv('C:\Users\kazef\Desktop\SINCOV-Streamlit\MD-Sincov\Data\dimparlamentar.csv')
convenio_dimension_df= pd.read_csv('C:\Users\kazef\Desktop\SINCOV-Streamlit\MD-Sincov\Data\dimconvenio.csv')
emenda_dimension_df= pd.read_csv('C:\Users\kazef\Desktop\SINCOV-Streamlit\MD-Sincov\Data\dimemenda.csv')
fatos_convenio_df = pd.read_csv('C:\Users\kazef\Desktop\SINCOV-Streamlit\MD-Sincov\Data\fatoconvenio.csv')



