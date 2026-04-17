import pandas as pd

def load_csv(filepath: str) -> pd.DataFrame:

    #Charge un fichier CSV et retourne un DataFrame.
    df = pd.read_csv(filepath)
    print(f"CSV chargé : {df.shape[0]} lignes, {df.shape[1]} colonnes")
    return df 


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
   
    print("clean data")
    #on enlève les doublons
    initial = len(df)
    df = df.drop_duplicates()
    print(f"Doublons supprimés : {initial - len(df)}")

    #on enlève les lignes sans nom de joueur
    if "player_name" in df.columns:
        df = df.dropna(subset=["player_name"])

    # On remplace les nan par 0
    df = df.fillna(0)

    return df

def age_group(age):
        if age < 22:
            return "Young"
        elif age < 28:
            return "Prime"
        else:
            return "Veteran"

def enrich_data(df: pd.DataFrame) -> pd.DataFrame:
    #créer des colonnes calculées utiles pour les analyses.
    
    # exemple créer un ratio points/minutes
    #if {"pts", "mp"}.issubset(df.columns):
    #    df["pts_per_min"] = df["pts"] / df["mp"].replace(0, 1)

    print("enrich data")

    df["points_per_game"] = df["pts"] / df["gp"]
    df["rebounds_per_game"] = df["reb"] / df["gp"]
    df["assists_per_game"] = df["ast"] / df["gp"]

    
    df["age_group"] = df["age"].apply(age_group)



    return df