from app.data_processing import load_csv, clean_data, enrich_data
from app.models import engine, init_db

def main():
    # Créer les tables
    init_db()

    # Charger le CSV
    df = load_csv("data/all_seasons.csv")

    # Nettoyer
    df = clean_data(df)

    # Enrichir
    df = enrich_data(df)

    # Envoyer en base dans la table player_stats
    # if_exists="replace" : on écrase à chaque fois
    df.to_sql("player_stats", engine, if_exists="replace", index=False)
    print("Données importées dans la table player_stats.")

if __name__ == "__main__":
    main()