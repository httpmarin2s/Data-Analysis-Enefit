# Data-Analysis-Enefit
Projeto Data Vikings | Dashboard com Python (Plotly e Streamlit) 
Projeto de Análise de Preços de Eletricidade

## Visão Geral

Este projeto tem como objetivo realizar uma análise de dados de preços de eletricidade (em euros por megawatt-hora, ou €MWh) ao longo do tempo, utilizando técnicas de visualização de dados para identificar padrões e tendências. O projeto envolve a leitura, tratamento e visualização de um conjunto de dados de preços de eletricidade, além da criação de análises temporais, de distribuição e padrões sazonais.

## Estrutura do Projeto

O projeto é composto pelas seguintes etapas:

1. **Importação de Bibliotecas**: Importação de bibliotecas necessárias como `pandas` para manipulação de dados, `numpy` para operações numéricas, e `plotly` para criação de gráficos interativos.
   
2. **Leitura dos Dados**: Carregamento dos dados de preços de eletricidade a partir de um arquivo CSV (`electricity_prices.csv`).

3. **Tratamento de Dados**: Transformação e criação de novas colunas, como ano, mês, dia e hora, a partir da coluna `forecast_date`, além da criação de uma coluna para agrupar dados por mês.

4. **Análise de Séries Temporais**: 
   - Cálculo da média diária dos preços de eletricidade.
   - Aplicação de médias móveis de 7 e 30 dias para suavizar a série temporal.
   - Visualização dos preços diários e suas médias móveis por meio de um gráfico de linhas.

5. **Análise de Distribuição (Boxplot)**: 
   - Criação de boxplots mensais para visualizar a distribuição dos preços ao longo dos meses.
   - Aplicação de filtros para remover outliers e garantir que os gráficos reflitam corretamente os dados.

6. **Mapa de Calor (Heatmap)**:
   - Criação de mapas de calor para analisar a relação entre o horário do dia e o preço médio de eletricidade.
   - O usuário pode gerar gráficos para meses e anos específicos para uma análise mais detalhada.

7. **Exportação de Dados**: 
   - Exportação dos dados tratados e resumidos em diferentes formatos parquet para fácil reutilização e armazenamento dos resultados.

## Dependências

Este projeto utiliza as seguintes bibliotecas:

- **pandas**: Para manipulação de dados.
- **numpy**: Para operações numéricas.
- **plotly**: Para visualização de dados (gráficos interativos).
- **warnings**: Para controlar alertas de warnings no código.

### Instalação de Dependências

Para rodar o projeto, certifique-se de ter as dependências instaladas. Utilize o seguinte comando para instalar os pacotes necessários:

```bash
pip install pandas numpy plotly
