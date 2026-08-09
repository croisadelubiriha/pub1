from flask import Flask, request, redirect, session
import psycopg2
import psycopg2.extras
import os
import html
import base64

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-cette-cle")

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


def get_connection():
    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL n'est pas configurée.")

    return psycopg2.connect(database_url)


def init_db():
    conn = get_connection()

    conn.execute("""
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
    conn.close()


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


def fichier_base64(fichier):
    if not fichier or not fichier.filename:
        return None

    contenu = fichier.read()

    if len(contenu) > 10 * 1024 * 1024:
        return None

    return base64.b64encode(contenu).decode("utf-8")


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
    margin: 4px;
}}

.delete {{
    background: #b00020;
}}

.edit {{
    background: #287a2b;
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

<p>Créé par Alphonse Kingereki</p>

<p>© 2026</p>

</footer>

</body>

</html>
"""


def afficher_media(photo, audio, video):

    media = ""

    if photo:
        media += f"""
        <img src="data:image/jpeg;base64,{photo}"
        alt="Photo">
        """

    if audio:
        media += f"""
        <audio controls>
            <source src="data:audio/mpeg;base64,{audio}">
        </audio>
        """

    if video:
        media += f"""
        <video controls>
            <source src="data:video/mp4;base64,{video}">
        </video>
        """

    return media


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

        media = afficher_media(photo, audio, video)

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

        <h3>
        ✝️ Pour nous aussi, le Christ !
        </h3>

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

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""
        SELECT id, categorie, titre, texte
        FROM contenus
        ORDER BY id DESC
    """)

    toutes = cur.fetchall()

    cur.close()
    conn.close()

    liste = ""

    for identifiant, categorie, titre, texte in toutes:

        nom_categorie = CATEGORIES.get(
            categorie,
            categorie
        )

        liste += f"""
        <div class="card">

            <h3>{html.escape(titre)}</h3>

            <p>
            <strong>{nom_categorie}</strong>
            </p>

            <p>
            {html.escape(texte).replace(chr(10), "<br>")}
            </p>

            <a href="/modifier/{identifiant}">
                <button class="edit">
                    ✏️ Modifier
                </button>
            </a>

            <form
                method="POST"
                action="/supprimer/{identifiant}"
                style="display:inline;"
                onsubmit="return confirm('Supprimer cette publication ?');">

                <button
                    type="submit"
                    class="delete">

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

            <form
                method="POST"
                action="/publier"
                enctype="multipart/form-data">

                <label>📂 Rubrique</label>

                <select
                    name="categorie"
                    required>

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

                <label>🖼️ Photo depuis le téléphone</label>

                <input
                    type="file"
                    name="photo"
                    accept="image/*">

                <label>🎵 Audio depuis le téléphone</label>

                <input
                    type="file"
                    name="audio"
                    accept="audio/*">

                <label>🎥 Vidéo depuis le téléphone</label>

                <input
                    type="file"
                    name="video"
                    accept="video/*">

                <button type="submit">
                    📢 PUBLIER
                </button>

            </form>

        </div>

        <h2>📋 Publications</h2>

        {liste}

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

    photo = fichier_base64(request.files.get("photo"))
    audio = fichier_base64(request.files.get("audio"))
    video = fichier_base64(request.files.get("video"))

    if categorie not in CATEGORIES:
        return "Rubrique invalide", 400

    if not titre or not texte:
        return "Titre et texte obligatoires", 400

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""
        INSERT INTO contenus
        (categorie, titre, texte, photo, audio, video)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        categorie,
        titre,
        texte,
        photo,
        audio,
        video
    ))

    conn.commit()

    cur.close()
    conn.close()

    return redirect("/dashboard")


@app.route("/supprimer/<int:identifiant>", methods=["POST"])
def supprimer(identifiant):

    if not session.get("admin"):
        return redirect("/admin")

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        "DELETE FROM contenus WHERE id = %s",
        (identifiant,)
    )

    conn.commit()

    cur.close()
    conn.close()

    return redirect("/dashboard")


@app.route("/modifier/<int:identifiant>", methods=["GET", "POST"])
def modifier(identifiant):

    if not session.get("admin"):
        return redirect("/admin")

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""
        SELECT id, categorie, titre, texte
        FROM contenus
        WHERE id = %s
    """, (identifiant,))

    publication = cur.fetchone()

    cur.close()
    conn.close()

    if not publication:
        return "Publication introuvable", 404

    if request.method == "POST":

        categorie = request.form.get("categorie", "")
        titre = request.form.get("titre", "").strip()
        texte = request.form.get("texte", "").strip()

        if categorie not in CATEGORIES:
            return "Rubrique invalide", 400

        if not titre or not texte:
            return "Titre et texte obligatoires", 400

        conn = get_connection()

        cur = conn.cursor()

        cur.execute("""
            UPDATE contenus
            SET categorie = %s, titre = %s, texte = %s
            WHERE id = %s
        """, (
            categorie,
            titre,
            texte,
            identifiant
        ))

        conn.commit()

        cur.close()
        conn.close()

        return redirect("/dashboard")

    _, categorie_actuelle, titre_actuel, texte_actuel = publication

    options = ""

    for c, n in CATEGORIES.items():

        selected = ""

        if c == categorie_actuelle:
            selected = "selected"

        options += f"""
        <option value="{c}" {selected}>
            {n}
        </option>
        """

    contenu = f"""

    <div class="card">

        <h2>✏️ Modifier la publication</h2>

        <form method="POST">

            <label>📂 Rubrique</label>

            <select
                name="categorie"
                required>

                {options}

            </select>

            <label>📝 Titre</label>

            <input
                type="text"
                name="titre"
                value="{html.escape(titre_actuel)}"
                required>

            <label>📄 Texte</label>

            <textarea
                name="texte"
                required>{html.escape(texte_actuel)}</textarea>

            <button type="submit">
                💾 Enregistrer
            </button>

        </form>

        <br>

        <a href="/dashboard">
            ↩️ Retour
        </a>

    </div>

    """

    return page("Modifier", contenu)


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
