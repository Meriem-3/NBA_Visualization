import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
#from app.data_processing import age_group

st.set_page_config(page_title="NBA Dashboard", layout="wide")

st.title(" NBA Dashboard — SportStats")

# Charger les données depuis l'API Flask
API_URL = "http://127.0.0.1:5000/api/data"

@st.cache_data
def load_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        st.error("Impossible de charger les données depuis l'API.")
        return pd.DataFrame()


def age_group(age):
        if age <= 24:
            return "Young"
        elif age < 29:
            return "Prime"
        else:
            return "Veteran"
        

df = load_data()
df["age_group"] = df["age"].apply(age_group)

#st.subheader("Aperçu des données")
#st.dataframe(df)


st.sidebar.header("Filtres")

teams = sorted(df["team_abbreviation"].dropna().unique())
seasons = sorted(df["season"].dropna().unique())
#positions = sorted(df["player_height"].dropna().unique())
ages = sorted(df["age"].dropna().unique())


age_filter = st.sidebar.selectbox("Âge", ["Tous"] + list(map(int, ages)))
team_filter = st.sidebar.selectbox("Équipe", ["Toutes"] + teams)
season_filter = st.sidebar.selectbox("Saison", ["Toutes"] + seasons)

filtered_df = df.copy()

if team_filter != "Toutes":
    filtered_df = filtered_df[df["team_abbreviation"] == team_filter]

if season_filter != "Toutes":
    filtered_df = filtered_df[df["season"] == season_filter]


if age_filter != "Tous":
    filtered_df = filtered_df[df["age"] == age_filter]



st.subheader("Données filtrées")
st.dataframe(filtered_df)

#csv 
st.download_button(
    label="Télécharger les données filtrées",
    data=filtered_df.to_csv(index=False),
    file_name="nba_filtered.csv",
    mime="text/csv"
)



#Visualisations


st.markdown(" Visualisations")


#Scatter Plot (Plotly)
if st.button("Relation entre âge et points marqués"):
    st.subheader("Relation entre âge et points marqués")
    fig_scatter = px.scatter(
        filtered_df,
        x="age",
        y="pts",
        color="team_abbreviation",
        hover_name="player_name",
        title="Âge vs Points marqués"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)


#Histogramme (Matplotlib)
if st.button("Distribution des points marqués"):
    st.subheader("Distribution des points marqués")
    fig, ax = plt.subplots()
    ax.hist(filtered_df["pts"], bins=20, color="skyblue", edgecolor="black")
    ax.set_xlabel("Points")
    ax.set_ylabel("Nombre de joueurs")
    ax.set_title("Histogramme des points")
    st.pyplot(fig)


#Bar Chart (Plotly)
if st.button("Top 10 joueurs par points"):

    st.subheader("Top 10 joueurs par points")
    top10 = filtered_df.nlargest(10, "pts")
    fig_bar = px.bar(
        top10,
        x="player_name",
        y="pts",
        color="pts",
        title="Top 10 joueurs (points)",
    )
    st.plotly_chart(fig_bar, use_container_width=True)


#Heatmap (Seaborn)
if st.button("Corrélation entre les statistiques"):

    st.subheader("Corrélation entre les statistiques")
    corr = filtered_df[["pts", "reb", "ast", "age"]].corr()
    fig2, ax2 = plt.subplots()
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax2)
    ax2.set_title("Heatmap des corrélations")
    st.pyplot(fig2)


#test boxplot
if st.button("Distribution des points par groupe d'âge"):

    st.subheader("Distribution des points par groupe d'âge")

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=filtered_df, x="age_group", y="pts", palette="Set2", ax=ax)
    ax.set_xlabel("Groupe d'âge")
    ax.set_ylabel("Points")
    st.pyplot(fig)

#test Barchart
if st.button("Moyenne des points par groupe d'âge"):

    st.subheader("Moyenne des points par groupe d'âge")

    avg_points = filtered_df.groupby("age_group")["pts"].mean().reset_index()

    fig = px.bar(
        avg_points,
        x="age_group",
        y="pts",
        color="age_group",
        title="Points moyens par groupe d'âge",
        text_auto=True
    )

    st.plotly_chart(fig)