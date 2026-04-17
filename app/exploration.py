import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

from app.models import engine

print("exploration.py lancé !")

def scatter_age_vs_points():
    
    df = pd.read_sql("SELECT age, pts FROM player_stats", engine)

    # On enlève les lignes avec age ou pts manquants
    df = df.dropna(subset=["age", "pts"])

    fig = px.scatter(
        df,
        x="age",
        y="pts",
        title="Relation entre âge et points marqués (NBA)"
    )
    fig.show()


def heatmap_correlations():
   
    df = pd.read_sql("SELECT pts, reb, ast, age FROM player_stats", engine)

    plt.figure(figsize=(6, 5))
    sns.heatmap(
        df.corr(),
        annot=True,
        cmap="coolwarm",
        center=0,
        fmt=".2f"
    )
    plt.title("Corrélation entre statistiques NBA")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    print("Bloc principal lancé.")
    scatter_age_vs_points()
    heatmap_correlations()