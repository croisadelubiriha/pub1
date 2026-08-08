from flask import Flask, request, redirect, session
import sqlite3
import os
import base64
import html

app = Flask(__name__)
app.secret_key = "change-cette-cle"

ADMIN_USER = "kingereki"
ADMIN_PASS = "alkinge@"

DB = "site.db"


# =========================
# BASE DE DONNÉES
# =========================

def init_db():
    conn = sqlite3.connect(DB)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS annonces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            texte TEXT NOT NULL,
            photo TEXT
        )
    """)

    conn.commit()
    conn.close()


def annonces():
    conn = sqlite3.connect(DB)

    resultats = conn.execute(
        "SELECT id, titre, texte, photo FROM annonces ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return resultats


# =========================
# DESIGN DU SITE
# =========================

def page(titre, contenu):

    return f"""
<!DOCTYPE html>
<html lang="fr">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1">

<title>{titre} - Croisade Eucharistique</title>

<style>

body {{
    margin:0;
    font-family:Arial,sans-serif;
    background:#f2f2f2;
    color:#222;
}}

header {{
    background:#123c69;
    color:white;
    text-align:center;
    padding:25px 10px;
}}

header h1 {{
    margin:10px 0;
}}

nav {{
    background:white;
    padding:12px 5px;
    text-align:center;
    box-shadow:0 2px 5px #bbb;
}}

nav a {{
    display:inline-block;
    margin:5px;
    padding:8px 10px;
    text-decoration:none;
    font-weight:bold;
    color:#123c69;
    border-radius:6px;
}}

nav a:hover {{
    background:#123c69;
    color:white;
}}

main {{
    max-width:900px;
    margin:auto;
    padding:20px;
}}

.card {{
    background:white;
    padding:20px;
    margin-bottom:18px;
    border-radius:12px;
    box-shadow:0 2px 7px #ccc;
}}

.card h2 {{
    color:#123c69;
}}

input,
textarea {{
    width:100%;
    padding:12px;
    margin:8px 0 15px;
    box-sizing:border-box;
    border:1px solid #ccc;
    border-radius:6px;
}}

textarea {{
    min-height:150px;
}}

button {{
    background:#123c69;
    color:white;
    border:0;
    padding:12px 18px;
    border-radius:6px;
    cursor:pointer;
}}

button:hover {{
    background:#0b2948;
}}

img {{
    max-width:100%;
    border-radius:10px;
    margin-top:10px;
}}

footer {{
    background:#123c69;
    color:white;
    text-align:center;
    padding:25px;
    margin-top:30px;
}}

.menu-title {{
    color:#123c69;
    font-weight:bold;
}}

</style>

</head>

<body>

<header>

<p>🇨🇩 RÉPUBLIQUE DÉMOCRATIQUE DU CONGO</p>

<p>DIOCÈSE DE BUTEMBO-BENI</p>

<p>PAROISSE SAINT CONRAD KASINDI</p>

<h1>✝️ CROISADE EUCHARISTIQUE</h1>

<h2>SECTEUR BON BERGER LUBIRIHA</h2>

</header>


<nav>

<a href="/">🏠 Accueil</a>

<a href="/servants">👥 Servants</a>

<a href="/classement">🏆 Classement</a>

<a href="/messes">🕐 Messes</a>

<a href="/enseignements">📚 Enseignements</a>

<a href="/croisade">✝️ Croisade</a>

<a href="/prieres">🙏 Prières</a>

<a href="/annonces">📢 Annonces</a>

<a href="/admin">👑 Admin</a>

</nav>


<main>

{contenu}

</main>


<footer>

<p>✝️ CROISADE EUCHARISTIQUE</p>

<p>SECTEUR BON BERGER LUBIRIHA</p>

<p>PAROISSE SAINT CONRAD KASINDI</p>

<p>Créé par Alphonse Kingereki</p>

<p>© 2026</p>

</footer>

</body>

</html>
"""


# =========================
# ACCUEIL
# =========================

@app.route("/")
def accueil():

    liste = ""

    for identifiant, titre, texte, photo in annonces():

        image = ""

        if photo:

            image = f'''
            <img src="data:image/jpeg;base64,{photo}">
            '''

        liste += f"""

        <div class="card">

            <h2>📢 {html.escape(titre)}</h2>

            {image}

            <p>
            {html.escape(texte).replace(chr(10), "<br>")}
            </p>

        </div>

        """

    if not liste:

        liste = """
        <div class="card">
            <p>Aucune annonce publiée pour le moment.</p>
        </div>
        """

    return page(
        "Accueil",

        f"""

        <div class="card">

            <h2>🙏 Bienvenue</h2>

            <p>
            Bienvenue sur le site officiel de la
            <strong>Croisade Eucharistique</strong>.
            </p>

            <p>
            Secteur Bon Berger Lubiriha,
            Paroisse Saint Conrad Kasindi,
            Diocèse de Butembo-Beni.
            </p>

        </div>


        <h2 class="menu-title">
        📢 Dernières annonces
        </h2>

        {liste}

        """
    )


# =========================
# SERVANTS
# =========================

@app.route("/servants")
def servants():

    return page(
        "Servants",

        """

        <div class="card">

            <h2>👥 Servants de Messe</h2>

            <p>
            Bienvenue dans l'espace des servants
            de la Croisade Eucharistique.
            </p>

            <h3>⛪ Notre mission</h3>

            <p>
            Servir Dieu avec foi, discipline,
            respect et amour de l'Église.
            </p>

            <h3>📚 Formation</h3>

            <p>
            Les servants participent régulièrement
            aux formations et activités de leur groupe.
            </p>

        </div>

        <div class="card">

            <h2>👤 Responsable</h2>

            <p>
            Les informations sur les responsables
            et les différents servants seront ajoutées
            prochainement.
            </p>

        </div>

        """
    )


# =========================
# CLASSEMENT
# =========================

@app.route("/classement")
def classement():

    return page(
        "Classement",

        """

        <div class="card">

            <h2>🏆 Classement des Servants</h2>

            <p>
            Cette page permettra de suivre
            les résultats et le classement
            des servants.
            </p>

        </div>

        <div class="card">

            <h3>🥇 1er</h3>
            <p>À compléter</p>

            <h3>🥈 2ème</h3>
            <p>À compléter</p>

            <h3>🥉 3ème</h3>
            <p>À compléter</p>

        </div>

        """
    )


# =========================
# MESSES
# =========================

@app.route("/messes")
def messes():

    return page(
        "Messes",

        """

        <div class="card">

            <h2>🕐 Horaires des Messes</h2>

            <h3>📅
