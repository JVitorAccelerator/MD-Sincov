from Classes import dataframe

df_convenio = dataframe.Dados.dimconvenio
df_data = dataframe.Dados.dimdata
df_emenda = dataframe.Dados.dimemenda
df_localizacao = dataframe.Dados.dimlocalizacao
df_parlamentar = dataframe.Dados.dimparlamentar
df_propostas = dataframe.Dados.dimproposta
df_fato = dataframe.Dados.fatoexecucao

df_convenio.to_parquet("./Data/dimconvenio.parquet")
df_data.to_parquet("./Data/dimdata.parquet")
df_emenda.to_parquet("./Data/dimemenda.parquet")
df_localizacao.to_parquet("./Data/dimlocalizacao.parquet")
df_parlamentar.to_parquet("./Data/dimparlamentar.parquet")
df_propostas.to_parquet("./Data/dimproposta.parquet")
df_fato.to_parquet("./Data/fatoexecucao.parquet")


