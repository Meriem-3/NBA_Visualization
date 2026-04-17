from flask import Flask, request, jsonify
import pandas as pd
from app.models import engine, Session, User
from app.auth import hash_password, verify_password, create_token
from dotenv import load_dotenv
import os


load_dotenv()#lit le fichier .env

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

#print(" API CHARGÉE : VERSION AVEC /api/stats ")

@app.route("/api/data")
def api_data():
    
    df = pd.read_sql("""
        SELECT player_name, team_abbreviation, age, pts, reb, ast, college, season
        FROM player_stats
    """, engine)

    # Filtre par équipe
    team = request.args.get("team")
    if team:
        df = df[df["team_abbreviation"] == team]

    # Filtre par college
    college = request.args.get("college")
    if college:
        df = df[df["college"] == college]

    # Filtre par min de points
    min_pts = request.args.get("min_pts")
    if min_pts:
        df = df[df["pts"] >= float(min_pts)]

    # Limite : ?limit=...
    limit = int(request.args.get("limit", 20000))
    df = df.head(limit)

    #renvoie une liste de dictionnaires
    return jsonify(df.to_dict(orient="records"))


@app.route("/api/stats")
def api_stats():

    #statistiques globales sur les joueurs
    
    df = pd.read_sql("""
        SELECT player_name, team_abbreviation, college, pts, reb, ast
        FROM player_stats
    """, engine)
    df = df.drop(columns=["Unnamed: 0"], errors="ignore")

    #Statistiques globales 
    stats_globales = {
        "moyenne_points": round(df["pts"].mean(), 2),
        "moyenne_rebonds": round(df["reb"].mean(), 2),
        "moyenne_assists": round(df["ast"].mean(), 2),
    }

    #  Top 5 colleges
    top_colleges = (
        df.groupby("college")["pts"]
        .mean()
        .sort_values(ascending=False)
        .head(5)
        .round(2)
        .to_dict()
    )

    #  Top 5 équipes 
    top_teams = (
        df.groupby("team_abbreviation")["pts"]
        .mean()
        .sort_values(ascending=False)
        .head(5)
        .round(2)
        .to_dict()
    )

    return jsonify({
        "stats_globales": stats_globales,
        "top_colleges": top_colleges,
        "top_teams": top_teams
    })



@app.route("/api/register", methods=["POST"])
def register():
    #Inscription
    data = request.json

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username et password requis"}), 400

    db = Session()

    #Vérifier si l'utilisateur existe déja
    if db.query(User).filter_by(username=username).first():
        return jsonify({"error": "Utilisateur déjà existant"}), 400

    # Créer l'utilisateur
    user = User(
        username=username,
        password_hash=hash_password(password)
    )

    db.add(user)
    db.commit()

    return jsonify({"message": "Utilisateur créé avec succès"})




@app.route("/api/login", methods=["POST"])
def login():
    
    data = request.json

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username et password requis"}), 400

    db = Session()

    #Vérifier les params
    #Vérifier si l'utilisateur existe
    user = db.query(User).filter_by(username=username).first()
    if not user:
        return jsonify({"error": "Utilisateur introuvable"}), 404

    #Vérifier le mot de passe
    if not verify_password(password, user.password_hash):
        return jsonify({"error": "Mot de passe incorrect"}), 401

    #Générer un token JWT
    token = create_token(user.id)

    return jsonify({
        "message": "Connexion réussie",
        "token": token
    })


if __name__ == "__main__":
    # Lancer l’API
    app.run(debug=True, port=5000)