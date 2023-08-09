import pandas as pd

class Dados:

    dimconvenio = pd.read_parquet("./Data/dimconvenio.parquet")
    dimdata = pd.read_parquet("./Data/dimdata.parquet")
    dimemenda = pd.read_parquet("./Data/dimemenda.parquet")
    dimlocalizacao = pd.read_parquet("./Data/dimlocalizacao.parquet")
    dimparlamentar = pd.read_parquet("./Data/dimparlamentar.parquet")
    dimproposta = pd.read_parquet("./Data/dimproposta.parquet")
    fatoexecucao = pd.read_parquet("./Data/fatoexecucao.parquet")