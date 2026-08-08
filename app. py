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


def page(titre, contenu):
    return f"""
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titre}</title>

<style>
body {{
    margin:0;
    font-family:Arial,sans-serif;
    background:#f2f2f2;
}}

header {{
    background:#123c69;
    color:white;
    text-align:center;
    padding:25px 10px;
}}

nav {{
    background:white;
    text-align:center;
    padding:12px;
}}

nav a {{
    margin:5px;
    text-decoration:none;
    font-weight:bold;
    color:#123c69;
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

input, textarea {{
    width:100%;
    padding:12px;
    margin:8px 0 15px;
    box-sizing:border-box;
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
    color:white;
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


@app.route("/")
def accueil():

    liste = ""

    for identifiant, titre, texte, photo in annonces():

        image = ""

        if photo:
            image = f'<img src="data:image/jpeg;base64,{photo}">'

        liste += f"""
        <div class="card">
            <h2>📢 {html.escape(titre)}</h2>
            {image}
            <p>{html.escape(texte).replace(chr(10), "<br>")}</p>
        </div>
        """

    if not liste:
        liste = "<p>Aucune annonce publiée pour le moment.</p>"

    return page(
        "Accueil",
        f"""
        <div class="card">
            <h2>🙏 Bienvenue</h2>
            <p>
            Bienvenue sur le site de la
            <strong>Croisade Eucharistique</strong>.
            </p>
        </div>

        <h2>📢 Dernières annonces</h2>

        {liste}
        """
    )


@app.route("/annonces")
def page_annonces():
    return accueil()


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

    liste = ""

    for identifiant, titre, texte, photo in annonces():

        image = ""

        if photo:
            image = f'<img src="data:image/jpeg;base64,{photo}">'

        liste += f"""
        <div class="card">

        <h3>📢 {html.escape(titre)}</h3>

        {image}

        <p>{html.escape(texte).replace(chr(10), "<br>")}</p>

        <form method="POST"
        action="/supprimer/{identifiant}">

        <button type="submit">
        🗑️ Supprimer
        </button>

        </form>

        </div>
        """

    return page(
        "Administration",
        f"""
        <div class="card">

        <h2>👑 Tableau de bord</h2>

        <h3>📢 Nouvelle publication</h3>

        <form method="POST"
        action="/publier"
        enctype="multipart/form-data">

        <label>Titre</label>

        <input
        type="text"
        name="titre"
        placeholder="Titre de l'annonce"
        required>

        <label>Information</label>

        <textarea
        name="texte"
        placeholder="Écris ton information ici..."
        required></textarea>

        <label>📷 Photo</label>

        <input
        type="file"
        name="photo"
        accept="image/*">

        <button type="submit">
        📢 PUBLIER
        </button>

        </form>

        </div>

        <h2>📋 Publications</h2>

        {liste}

        <div class="card">
        <a href="/logout">🚪 Déconnexion</a>
        </div>
        """
    )


@app.route("/publier", methods=["POST"])
def publier():

    if not session.get("admin"):
        return redirect("/admin")

    titre = request.form.get("titre", "").strip()
    texte = request.form.get("texte", "").strip()

    photo = request.files.get("photo")
    photo_base64 = None

    if photo and photo.filename:

        contenu = photo.read()

        if len(contenu) <= 2 * 1024 * 1024:
            photo_base64 = base64.b64encode(contenu).decode("utf-8")

    if titre and texte:

        conn = sqlite3.connect(DB)

        conn.execute(
            """
            INSERT INTO annonces
            (titre, texte, photo)
            VALUES (?, ?, ?)
            """,
            (titre, texte, photo_base64)
        )

        conn.commit()
        conn.close()

    return redirect("/dashboard")


@app.route("/supprimer/<int:identifiant>", methods=["POST"])
def supprimer(identifiant):

    if not session.get("admin"):
        return redirect("/admin")

    conn = sqlite3.connect(DB)

    conn.execute(
        "DELETE FROM annonces WHERE id = ?",
        (identifiant,)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/admin")


init_db()


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
    )
