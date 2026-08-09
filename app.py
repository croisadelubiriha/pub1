from flask import Flask, request, redirect, session
import psycopg2
import os
import html
import base64

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "change-cette-cle"
)

ADMIN_USER = "kingereki"
ADMIN_PASS = "alkinge@"

CATEGORIES = {
    "servants": "👥 Servants",
    "classement": "🏆 Classement",
    "messes": "🕐 Messes",
    "enseignements": "📚 Enseignements",
    "croisade": "✝️ Croisade",
    "prieres": "🙏 Prières",
    "annonces": "📢 Annonces",
    "diverses": "📰 Diverses"
}


# =========================
# CONNEXION À POSTGRESQL
# =========================

def get_connection():

    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "DATABASE_URL n'est pas configurée dans Render."
        )

    return psycopg2.connect(database_url)


# =========================
# CREATION DE LA TABLE
# =========================

def init_db():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS contenus (
            id SERIAL PRIMARY KEY,
            categorie TEXT NOT NULL,
            titre TEXT NOT NULL,
            texte TEXT NOT NULL,
            photo TEXT,
            audio TEXT,
            video TEXT
        )
    """)

    conn.commit()

    cur.close()
    conn.close()


# =========================
# RECUPERER LES PUBLICATIONS
# =========================

def get_contenus(categorie):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, titre, texte, photo, audio, video
        FROM contenus
        WHERE categorie = %s
        ORDER BY id DESC
    """, (categorie,))

    resultats = cur.fetchall()

    cur.close()
    conn.close()

    return resultats


# =========================
# FICHIER EN BASE64
# =========================

def fichier_base64(fichier):

    if not fichier or not fichier.filename:
        return None

    contenu = fichier.read()

    # Limite de 10 MB
    if len(contenu) > 10 * 1024 * 1024:
        return None

    return base64.b64encode(
        contenu
    ).decode("utf-8")


# =========================
# PAGE PRINCIPALE
# =========================

def page(titre, contenu):

    menu = ""

    for url, nom in CATEGORIES.items():

        menu += f"""
        <a href="/{url}">
            {nom}
        </a>
        """

    return f"""
<!DOCTYPE html>

<html lang="fr">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1">

<title>{html.escape(titre)}</title>

<style>

body {{
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f2f2f2;
}}

header {{
    background: #123c69;
    color: white;
    text-align: center;
    padding: 25px 10px;
}}

header p {{
    margin: 6px;
}}

header h1 {{
    margin: 12px 0 5px;
}}

header h2 {{
    margin: 5px 0;
}}

nav {{
    background: white;
    padding: 10px;
    text-align: center;
}}

nav a {{
    display: inline-block;
    margin: 4px;
    padding: 9px;
    text-decoration: none;
    font-weight: bold;
    color: #123c69;
    border-radius: 6px;
}}

nav a:hover {{
    background: #eeeeee;
}}

main {{
    max-width: 900px;
    margin: auto;
    padding: 20px;
}}

.card {{
    background: white;
    padding: 20px;
    margin-bottom: 18px;
    border-radius: 12px;
    box-shadow: 0 2px 7px #ccc;
}}

input,
textarea,
select {{
    width: 100%;
    box-sizing: border-box;
    padding: 12px;
    margin: 8px 0 15px;
    border: 1px solid #ccc;
    border-radius: 6px;
}}

textarea {{
    min-height: 150px;
}}

button {{
    background: #123c69;
    color: white;
    border: 0;
    padding: 12px 18px;
    border-radius: 6px;
    margin: 4px;
    cursor: pointer;
}}

.delete {{
    background: #b00020;
}}

.edit {{
    background: #287a2b;
}}

img {{
    max-width: 100%;
    height: auto;
    border-radius: 10px;
    margin-top: 10px;
}}

audio {{
    width: 100%;
    margin-top: 10px;
}}

video {{
    width: 100%;
    max-height: 500px;
    margin-top: 10px;
}}

footer {{
    background: #123c69;
    color: white;
    text-align: center;
    padding: 25px;
    margin-top: 30px;
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

{menu}

<a href="/admin">👑 Admin</a>

</nav>

<main>

{contenu}

</main>

<footer>

<p>✝️ CROISADE EUCHARISTIQUE</p>

<p>SECTEUR BON BERGER LUBIRIHA</p>

<p>Créé par Alphonse Kingereki</p>

<p>© 2026</p>

</footer>

</body>

</html>
"""


# =========================
# AFFICHER PHOTO AUDIO VIDEO
# =========================

def afficher_media(photo, audio, video):

    media = ""

    if photo:

        media += f"""
        <img
            src="data:image/jpeg;base64,{photo}"
            alt="Photo">
        """

    if audio:

        media += f"""
        <audio controls>
            <source
                src="data:audio/mpeg;base64,{audio}">
            Votre navigateur ne supporte pas l'audio.
        </audio>
        """

    if video:

        media += f"""
        <video controls>
            <source
                src="data:video/mp4;base64,{video}">
            Votre navigateur ne supporte pas la vidéo.
        </video>
        """

    return media


# =========================
# AFFICHER UNE RUBRIQUE
# =========================

def afficher_contenus(categorie):

    nom = CATEGORIES[categorie]

    liste = get_contenus(categorie)

    contenu = f"""
    <div class="card">

        <h2>{nom}</h2>

        <p>
        Bienvenue dans cette rubrique.
        </p>

    </div>
    """

    if not liste:

        contenu += """
        <div class="card">

            <p>
            Aucune publication pour le moment.
            </p>

        </div>
        """

    for identifiant, titre, texte, photo, audio, video in liste:

        media = afficher_media(
            photo,
            audio,
            video
        )

        contenu += f"""
        <div class="card">

            <h2>
                {html.escape(titre)}
            </h2>

            {media}

            <p>
                {html.escape(texte).replace(
                    chr(10),
                    "<br>"
                )}
            </p>

        </div>
        """

    return page(
        nom,
        contenu
    )


# =========================
# ACCUEIL
# =========================

@app.route("/")
def accueil():

    contenu = """

    <div class="card">

        <h2>🙏 Bienvenue</h2>

        <p>
        Bienvenue sur le site de la
        <strong>Croisade Eucharistique</strong>.
        </p>

        <p>
        Secteur Bon Berger Lubiriha.
        </p>

        <h3>
        ✝️ Pour nous aussi, le Christ !
        </h3>

    </div>

    """

    return page(
        "Accueil",
        contenu
    )


# =========================
# ADMIN
# =========================

@app.route(
    "/admin",
    methods=["GET", "POST"]
)
def admin():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        )

        password = request.form.get(
            "password",
            ""
        )

        if (
            username == ADMIN_USER
            and password == ADMIN_PASS
        ):

            session["admin"] = True

            return redirect(
                "/dashboard"
            )

        return page(
            "Erreur",
            """
            <div class="card">

                <h2>
                    ❌ Identifiants incorrects
                </h2>

                <a href="/admin">
                    Retour
                </a>

            </div>
            """
        )

    return page(
        "Administration",
        """

        <div class="card">

            <h2>
                👑 Espace Administrateur
            </h2>

            <form method="POST">

                <label>
                   
