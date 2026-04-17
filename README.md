

Projet réalisé par Meriam Chebbi 
Objectif : analyser les performances NBA et créer un dashboard interactif et sécurisé.


# 🏀 NBA Player Insights – API + Dashboard Streamlit

Ce projet a été créé pour analyser les performances des joueurs NBA de manière simple, visuelle et interactive.  
L’objectif principal est de répondre à des questions comme :

- Quels sont les joueurs les plus performants ?
- Comment l’âge influence-t-il les points marqués ?
- Les joueurs “jeunes”, “dans leur prime” ou “vétérans” performent-ils différemment ?

Le projet combine un pipeline de données, une API sécurisée et un dashboard interactif.

---


Créer un environnement virtuel
    python -m venv .venv
Activer l’environnement
    .venv\Scripts\activate
Installer les dépendances
    pip install -r requirements.txt
        OU
    python -m pip install -r requirements.txt
    
Configuration (.env)

Créer un fichier `.env` **à la racine du projet** :
    SECRET_KEY=ta_cle_secrete_ici
    DATABASE_URL=sqlite:///sportstats.db

La SECRET_KEY sert à signer les tokens JWT.  
On ne la met jamais dans le code pour des raisons de sécurité.

---

-- Lancer l’API Flask
    python app/api.py


L’API expose plusieurs routes :

- `/api/login` → renvoie un token JWT  
- `/api/data` → renvoie les données (protégée)  
- `/api/stats` → statistiques agrégées  


---

Lancer le dashboard Streamlit
    streamlit run dashboard.py
    

Le dashboard permet :

- de filtrer les joueurs (équipe, saison, points minimum…)  
- d’afficher plusieurs visualisations interactives  
- d’explorer les relations entre âge, points et groupes d’âge  
- d’afficher certains graphiques uniquement lorsqu’on clique sur un bouton  
- d’exporter les données filtrées  

---

##  Visualisations principales

###  Scatter Plot : Âge vs Points  
Permet de voir comment les performances évoluent avec l’âge.  
On observe facilement :
- les jeunes marquent moins  
- les joueurs dans leur “prime” performent le mieux  
- les vétérans déclinent légèrement  

###  Bar Chart : Moyenne des points par groupe d’âge  
Grâce à la colonne `age_group` (Young / Prime / Veteran),  
on peut comparer les performances moyennes par tranche d’âge.

###  Boxplot : Distribution des points par groupe d’âge  
Montre la dispersion des performances selon les tranches d’âge.(pas trop utile)

###  Autres visuels (selon le dataset)
- Heatmap des corrélations  
- Classement des 10 meilleurs joueurs  
 

---

##  Pipeline de données

### 1. Nettoyage (clean_data)
- suppression des doublons  
- gestion des valeurs manquantes  
- conversion des types numériques  

### 2. Enrichissement (enrich_data)
- points_per_game  
- rebounds_per_game  
- assists_per_game  
- age_group (catégorisation des joueurs)  

---

## 🔒 Sécurité

- Hashage des mots de passe avec **bcrypt**  
- Authentification via **JWT**  
- SECRET_KEY stockée dans `.env`   
- ORM SQLAlchemy → protège contre les injections SQL  



