from flask import Flask, render_template, request, redirect, url_for
import cloudinary
import cloudinary.uploader
import sqlite3
from werkzeug.utils import secure_filename
from PIL import Image
import io
import os
import random

app = Flask(__name__)

# Configuración Cloudinary
cloudinary.config(
    cloud_name="TU_CLOUD_NAME",
    api_key="TU_API_KEY",
    api_secret="TU_API_SECRET"
)

DB_PATH = "fotos.db"

# Inicializar DB
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS fotos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mesa TEXT,
            persona TEXT,
            filename TEXT,
            url TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/subir", methods=["GET", "POST"])
def subir():
    if request.method == "POST":
        mesa = request.form.get("mesa")
        persona = request.form.get("persona")
        files = request.files.getlist("files")

        if not mesa or not persona or not files:
            return "Faltan datos", 400

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM fotos WHERE persona = ?", (persona,))
        count = c.fetchone()[0]

        if count + len(files) > 20:
            conn.close()
            return "<script>alert('Máximo 20 fotos por persona'); window.history.back();</script>"

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(f"{persona}_{file.filename}")

                # Redimensionar y comprimir
                img = Image.open(file)
                img.thumbnail((1080, 1080))
                buffer = io.BytesIO()
                img.save(buffer, format="JPEG", quality=85)
                buffer.seek(0)

                # Subir a Cloudinary
                result = cloudinary.uploader.upload(buffer, public_id=filename)
                url = result['secure_url']

                c.execute("INSERT INTO fotos (mesa, persona, filename, url) VALUES (?,?,?,?)",
                          (mesa, persona, filename, url))

        conn.commit()
        conn.close()
        return redirect(url_for("album", mesa=mesa))

    return render_template("index.html")

@app.route("/album/<mesa>")
def album(mesa):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT persona, filename, url FROM fotos WHERE mesa=?", (mesa,))
    fotos = c.fetchall()
    conn.close()
    return render_template("album.html", fotos=fotos, mesa=mesa)

@app.route("/inicio")
def inicio():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT mesa, persona, filename, url FROM fotos")
    all_fotos = c.fetchall()
    conn.close()
    if len(all_fotos) > 50:
        fotos = random.sample(all_fotos, 50)
    else:
        fotos = all_fotos
    return render_template("inicio.html", fotos=fotos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)

