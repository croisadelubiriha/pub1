from flask import Flask, request, redirect, session
import sqlite3
import os
import html

app = Flask(__name__)
app.secret_key = "change-cette-cle"

ADMIN_USER = "kingereki"
ADMIN_PASS = "alkinge@"

DB = "site.db"

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


def init_db():
    conn = sqlite3.connect(DB)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS contenus (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categorie TEXT NOT NULL,
            titre TEXT NOT NULL,
            texte TEXT NOT NULL,
            photo TEXT,
            audio TEXT,
            video TEXT
        )
    """)

    conn.commit()
    conn.close()


def get_contenus(categorie):
    conn = sqlite3.connect(DB)

    resultats = conn.execute("""
        SELECT id, titre, texte, photo, audio, video
        FROM contenus
        WHERE categorie = ?
        ORDER BY id DESC
    """, (categorie,)).fetchall()

    conn.close()

    return resultats


def page(titre, contenu):

    menu = ""

    for url, nom in CATEGORIES.items():
        menu += f'<a href="/{url}">{nom}</a>'

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

nav {{
    background: white;
    padding: 10px;
    text-align: center;
}}

nav a {{
    display: inline-block;
    margin: 4px;
    padding: 8px;
    text-decoration: none;
    font-weight: bold;
    color: #123c69;
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
}}

img {{
    max-width: 100%;
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

<p>PAROISSE SAINT CONRAD KASINDI</p>

<p>Créé par Alphonse Kingereki</p>

<p>© 2026</p>

</footer>

</body>

</html>
"""


def afficher_contenus(categorie):

    nom = CATEGORIES[categorie]

    liste = get_contenus(categorie)

    contenu = f"""
    <div class="card">
        <h2>{nom}</h2>
        <p>Bienvenue dans cette rubrique.</p>
    </div>
    """

    if not liste:

        contenu += """
        <div class="card">
            <p>Aucune publication pour le moment.</p>
        </div>
        """

    for identifiant, titre, texte, photo, audio, video in liste:

        media = ""

        if photo:
            media += f"""
            <img src="{html.escape(photo)}" alt="Photo">
            """

        if audio:
            media += f"""
            <audio controls>
                <source src="{html.escape(audio)}">
            </audio>
            """

        if video:
            media += f"""
            <video controls>
                <source src="{html.escape(video)}">
            </video>
            """

        contenu += f"""
        <div class="card">

            <h2>{html.escape(titre)}</h2>

            {media}

            <p>
            {html.escape(texte).replace(chr(10), "<br>")}
            </p>

        </div>
        """

    return page(nom, contenu)


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

        <p>
        ✝️ Pour nous aussi, le Christ !
        </p>

    </div>
    """

    return page("Accueil", contenu)


@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if username == ADMIN_USER and password == ADMIN_PASS:

            session["admin"] = True

            return redirect("/dashboard")

        return page(
            "Erreur",
            """
            <div class="card">
                <h2>❌ Identifiants incorrects</h2>
                <a href="/admin">Retour</a>
            </div>
            """
        )

    return page(
        "Administration",
        """
        <div class="card">

            <h2>👑 Espace Administrateur</h2>

            <form method="POST">

                <label>Nom administrateur</label>

                <input
                    type="text"
                    name="username"
                    required>

                <label>Mot de passe</label>

                <input
                    type="password"
                    name="password"
                    required>

                <button type="submit">
                    🔐 Connexion
                </button>

            </form>

        </div>
        """
    )


@app.route("/dashboard")
def dashboard():

    if not session.get("admin"):
        return redirect("/admin")

    return page(
        "Administration",
        f"""
        <div class="card">

            <h2>👑 Tableau de bord</h2>

            <h3>➕ Nouvelle publication</h3>

            <form method="POST"
                  action="/publier">

                <label>📂 Rubrique</label>

                <select name="categorie" required>

                    {
                    ''.join(
                        f'<option value="{c}">{n}</option>'
                        for c, n in CATEGORIES.items()
                    )
                    }

                </select>

                <label>📝 Titre</label>

                <input
                    type="text"
                    name="titre"
                    required>

                <label>📄 Texte</label>

                <textarea
                    name="texte"
                    required></textarea>

                <label>🖼️ Lien de la photo</label>

                <input
                    type="url"
                    name="photo"
                    placeholder="https://...">

                <label>🎵 Lien de l'audio</label>

                <input
                    type="url"
                    name="audio"
                    placeholder="https://...">

                <label>🎥 Lien de la vidéo</label>

                <input
                    type="url"
                    name="video"
                    placeholder="https://...">

                <button type="submit">
                    📢 PUBLIER
                </button>

            </form>

        </div>

        <div class="card">

            <h3>📋 Gestion des publications</h3>

            <p>
            Les publications sont enregistrées
            dans la rubrique choisie.
            </p>

        </div>

        <div class="card">

            <a href="/logout">
                🚪 Déconnexion
            </a>

        </div>
        """
    )


@app.route("/publier", methods=["POST"])
def publier():

    if not session.get("admin"):
        return redirect("/admin")

    categorie = request.form.get("categorie", "")
    titre = request.form.get("titre", "").strip()
    texte = request.form.get("texte", "").strip()
    photo = request.form.get("photo", "").strip()
    audio = request.form.get("audio", "").strip()
    video = request.form.get("video", "").strip()

    if categorie not in CATEGORIES:
        return "Rubrique invalide", 400

    if not titre or not texte:
        return "Titre et texte obligatoires", 400

    conn = sqlite3.connect(DB)

    conn.execute("""
        INSERT INTO contenus
        (categorie, titre, texte, photo, audio, video)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        categorie,
        titre,
        texte,
        photo or None,
        audio or None,
        video or None
    ))

    conn.commit()
    conn.close()

    return redirect("/dashboard")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/admin")


for categorie in CATEGORIES:

    app.add_url_rule(
        f"/{categorie}",
        endpoint=f"page_{categorie}",
        view_func=lambda categorie=categorie:
            afficher_contenus(categorie)
    )


init_db()


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
    )
