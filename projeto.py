# Importando bibliotecas necessárias
import pandas as pd 
import numpy as np 

import plotly.express as px 
import plotly.graph_objects as go 
from plotly.subplots import make_subplots

import warnings 
warnings.filterwarnings('ignore')

# Lendo o dataframe 
base_eletricidade = pd.read_csv('electricity_prices.csv')

base_eletricidade.head()

# Tratamento dos dados
base_eletricidade.forecast_date = pd.to_datetime( base_eletricidade.forecast_date )

base_eletricidade['ano'] = base_eletricidade.forecast_date.dt.year
base_eletricidade['mes'] = base_eletricidade.forecast_date.dt.month
base_eletricidade['dia'] = base_eletricidade.forecast_date.dt.day
base_eletricidade['data'] = base_eletricidade.forecast_date.dt.date
base_eletricidade['hora'] = base_eletricidade.forecast_date.dt.hour

base_eletricidade.head()

## Análise inicial
anl_media_preco = base_eletricidade.groupby( by=['data']). agg(
    media_preco = ('euros_per_mwh', 'mean')
)

anl_media_preco['mm30d'] = anl_media_preco.media_preco.rolling(window=30).mean()
anl_media_preco['mm7d'] = anl_media_preco.media_preco.rolling(window=7).mean()
#Agrupa os dados por cada valor único da coluna data e calcula a média de preço por hora

anl_media_preco.head()

## Montagem do gráfico
# Criar figura
Figura = go.Figure()

# Adicionar série temporal diária
Figura.add_trace(
    go.Scatter(
        x=anl_media_preco.index,
        y=anl_media_preco['media_preco'],
        mode='lines',
        name='Diário',
        line=dict(color='#adadad')
    )
)

# Adicionar média móvel de 7 dias
Figura.add_trace(
    go.Scatter(
        x=anl_media_preco.index,
        y=anl_media_preco['mm7d'],
        mode='lines',
        name='mm7d',
        line=dict(color='blue', width=2)
    )
)

# Adicionar média móvel de 30 dias com janela rolante de 20 dias
Figura.add_trace(
    go.Scatter(
        x=anl_media_preco.index,
        y=anl_media_preco['mm30d'].rolling(window=20).mean(),
        mode='lines',
        name='mm30d',
        line=dict(color='#4f390b', width=3)
    )
)

# Títulos e labels
Figura.update_layout(
    title='Série Temporal | Preço megawatt-hora (MWh) €',
    xaxis_title='Data',
    yaxis_title='Preço em EURO €',
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='center',
        x=0.5,
    ),
    height=600,
    width=1200
)

## Box plot 
base_eletricidade['data_boxplot'] = base_eletricidade['ano'].astype('str') + '-' + base_eletricidade['mes'].astype('str')
base_eletricidade.head()

dados_filtrados = base_eletricidade.loc[base_eletricidade['euros_per_mwh'] < 4000]

# Criar figura
Figura2 = go.Figure()

# Adicionar um boxplot para cada mês (assumindo que 'data_boxplot' contém a categoria mensal)
for categoria in dados_filtrados['data_boxplot'].unique():

    Figura2.add_trace(go.Box(
        y=dados_filtrados[dados_filtrados['data_boxplot'] == categoria]['euros_per_mwh'],
        name=categoria,
        boxmean='sd',  # Para mostrar a média e desvio padrão no boxplot
        width=0.5,
        marker_color='#636efa'
    ))

# Títulos e labels
Figura2.update_layout(
    title='Distribuição de Preço megawatt-hora (MWh) € | Mensal',
    xaxis_title='Mês',
    yaxis_title='Preço em EURO €',
    xaxis={'type': 'category'},  # Para garantir que os meses sejam categóricos
    height=500,
    width=1200,
    showlegend=False
)

# Rotacionar os rótulos do eixo x
Figura2.update_xaxes(tickangle=90)

## Mapa de calor 

def gerar_grafico_estudo( dados, ano, mes ):

  # Filtrar o ano e mes que o usuário está setando no FRONT-END
  Filtro = dados.loc[ (dados.ano == ano) & (dados.mes == mes) ]

  # Analise
  anl_estudo = Filtro.groupby( by=['dia', 'hora'] ).agg(
    media_preco = ('euros_per_mwh', 'mean')
  ).reset_index()

  # Pivotar a tabela
  anl_estudo = anl_estudo.pivot_table( index='hora', columns='dia', values='media_preco')

  # Ordenacao
  anl_estudo = anl_estudo.sort_index()

  # Ajuste no index
  anl_estudo.index = anl_estudo.index.astype(str)

  # Criar heatmap
  Figura3 = go.Figure(
      data=go.Heatmap(
        z=anl_estudo.values,
        x=anl_estudo.columns,
        y=anl_estudo.index,
        colorscale='Reds',
        showscale=True,
        colorbar=dict(thickness=10, len=0.25)
    )
  )

  # Títulos e labels
  Figura3.update_layout(
      title=f'Mapa de Calor {ano}, comparação dias x meses',
      xaxis_title='Dias',
      yaxis_title='Horário',
      height=700,
      width=900
  )

  return Figura3

gerar_grafico_estudo(base_eletricidade, 2022, 1)

# Analise horário vs dia
base_eletricidade.loc[ (base_eletricidade.ano == 2023) & (base_eletricidade.mes == 1) ].groupby(
    by=['dia', 'hora'] ).agg(
      media_preco = ('euros_per_mwh', 'mean')
        ).reset_index().pivot_table(
            index='hora', columns='dia', values='media_preco')

# Analise horário vs dia
anl_horaDia = base_eletricidade.loc[ base_eletricidade.ano == 2023 ].groupby(
    by=['dia', 'hora'] ).agg(
      media_preco = ('euros_per_mwh', 'mean')
        ).reset_index().pivot_table(
            index='hora', columns='dia', values='media_preco')

# ajustando index
anl_horaDia = anl_horaDia.sort_index()
anl_horaDia.index = anl_horaDia.index.astype(str)

anl_horaDia.head()

# Criar heatmap
Figura3 = go.Figure(data=go.Heatmap(
    z=anl_horaDia.values,
    x=anl_horaDia.columns,
    y=anl_horaDia.index,
    colorscale='Reds',
    showscale=True,
    colorbar=dict(thickness=10, len=0.25)  # Shrink colorbar
))

# Títulos e labels
Figura3.update_layout(
    title='Mapa de Calor 2023, comparação dias x  hora',
    xaxis_title='Dias',
    yaxis_title='Horário',
    height=700,
    width=900
)

anl_media_bigNumber = base_eletricidade.groupby( by=['ano'] ).agg( media= ('euros_per_mwh', 'mean') ).reset_index()

anl_media_2024 = pd.DataFrame({
    'ano' : 2024,
    'media' : base_eletricidade['euros_per_mwh'].mean()
}, index=[0])

anl_media_bigNumber = pd.concat( [anl_media_bigNumber, anl_media_2024] )

anl_media_bigNumber

anl_media_bigNumber.to_parquet('dados_bignumber.parquet')
anl_media_preco.to_parquet('dados_serietemporal.parquet')
dados_filtrados[['euros_per_mwh', 'data_boxplot']].to_parquet('dados_boxplot.parquet')
base_eletricidade[['ano', 'mes', 'dia', 'hora', 'euros_per_mwh']].to_parquet('dados_estudo.parquet')