import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

#Importação do DataSet
def importar_data_set():
    df = pd.read_csv("Dd5e_monsters.csv")
    return df

#Ajeitando as colunas e organizando os dados
def mudar_nome_das_colunas(df):
    df.columns = ('Nome', 'Tamanho', "Raça + Alinhamento", "HP", "CA", "Deslocamento", "CR")

def separar_colunas(df):
    df['XP'] = df["CR"].apply(lambda x : x.split("(")[1].split(")")[0])
    df['CR'] = df["CR"].apply(lambda x : x.split(" ")[0])
    df['Raça'] = df["Raça + Alinhamento"].apply(lambda x : x.split(",")[0])
    df['Alinhamento'] = df["Raça + Alinhamento"].apply(lambda x : x.split(",")[1])

def remover_colunas_desnecessarias(df):
    df.drop(columns=["Raça + Alinhamento"], inplace=True)

#Mudando os tipos de dado
def mudar_tipos_de_dado(df):
    df['CA'] = df['CA'].apply(lambda x : x.split(' ')[0]).astype(int)
    df['HP'] = df['HP'].apply(lambda x : x.split(' ')[0]).astype(int)
    df['XP'] = df['XP'].apply(lambda x : x.split(' ')[0])

    cont = 0
    for i in df['XP']:
        if ',' in i:
            df["XP"].replace(df["XP"][cont], df["XP"][cont].split(",")[0] + df["XP"][cont].split(",")[1], inplace=True)
        cont+=1

    df['XP'] = df['XP'].astype(int)

    cont = 0
    for i in df['CR']:
        if '/' in i:
            df["CR"].replace(df['CR'][cont], str(float(df['CR'][cont].split("/")[0])  /  float(df['CR'][cont].split("/")[1])), inplace=True)
        cont+=1

    df['CR'] = df['CR'].astype(float)

#Estatísticas Descritivas
def mostrar_descritivas(df):
    print(df.describe())
    df.info()

#Tratamento de dados
# Não encontramos dados faltantes, apenas separamos os dados de maneira mais organizada e mudamos os tipos de alguns dados para tipos mais apropriados.

#Remoção de Outliers
# A remoção de outliers prejudicaria o resultado final do dataset, pois o objetivo aqui é contemplar todos os monstros de D&D, independentemente da diferença de características entre eles.

#Planejamento do DashBoard
# Nosso público alvo são os jogadores de D&D, então planejamos criar um dashboard que permita uma boa visualização dos principais mosntros do jogo e quais seus status. Também queremos permitir que o jogador escolha monstros de nível adequado para as suas mesas de RPG levando em conta o nível de dificuldade e atributos do monstro.

#Novas Colunas
def criar_coluna_categoria(df):
    df['Categoria'] = df['CR'].apply(lambda x : 'Básico' if x < 3 else('Intermediário' if x < 7 else('Mini Chefe' if x < 10 else 'Chefão')))

#DashBoard
def dash_board(df):

    st.header("Monstros D&D")

    st.subheader("Insira uma das informações disponíveis nas caixas:\nNome, Tamanho, Raça, Alinhamento, HP, CA, Deslocamento, CR, Categoria")

    res1 = st.text_input('Insira uma informação','Nome')
    res2 = st.text_input('Insira uma informação','Categoria')

    if res1 not in df.columns or res2 not in df.columns:

        st.text('Nomes inválidos')

    else:

        on = st.toggle('Gráfico de Pontos')

        if on:
            fig = px.scatter(x=df[res1], y=df[res2])
            fig.update_traces(marker=dict(color="lightgreen"))
            fig.update_layout(
                xaxis_title=f"{res1}",
                yaxis_title=f"{res2}"
            )
            
        else:
            fig = px.bar(x=df[res1], y=df[res2])
            fig.update_traces(marker=dict(color="rosybrown"))
            fig.update_layout(
                xaxis_title=f"{res1}",
                yaxis_title=f"{res2}"
            )

        st.plotly_chart(fig)

    res3 = st.text_input('Busque um nome','Aboleth')

    if res3 not in df['Nome'].values:
        st.text('Nome inválido')

    else:
        status = ['HP', 'CA', "CR"]

        data = df[df['Nome'] == res3]

        valores = data[status].iloc[0]

        fig2 = px.bar(x=status, y= valores)
        fig2.update_traces(marker=dict(color="yellow"))
        fig2.update_layout(
                xaxis_title=f"Status",
                yaxis_title=f"Valores"
            )

        st.plotly_chart(fig2)

    res4 = st.text_input('Monstros com XP maior que','300')
    res5 = st.text_input('e menor que','800')

    if res4 == '' or res5 == '' or res4 > res5 or res5 < res4:
        st.text('Valores inválidos')
    else:
        valores = df[(df["XP"] >= int(res4)) & (df["XP"] <= int(res5))]

        fig3 = px.bar(valores,x="Nome", y= "XP")
        fig3.update_traces(marker=dict(color="yellow"))
        fig3.update_layout(
                xaxis_title=f"XP",
                yaxis_title=f"Nomes"
            )

        st.plotly_chart(fig3)



def main():
    df = importar_data_set()
    mudar_nome_das_colunas(df)
    separar_colunas(df)
    remover_colunas_desnecessarias(df)
    mudar_tipos_de_dado(df)

    print("Dados Quantitativos / Moda / Média / Mediana / Desvio-Padrão / Contagem")

    mostrar_descritivas(df)

    criar_coluna_categoria(df)

    dash_board(df)

if __name__ == '__main__':
    main()
