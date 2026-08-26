import os
from flask import Flask, jsonify

app = Flask(__name__)

# Jeu de donnees de secours, utilise quand aucune base n'est configuree.
RELEVES_SECOURS = [
    {"ville": "Paris", "temperature": 21},
    {"ville": "Lyon", "temperature": 24},
    {"ville": "Marseille", "temperature": 27},
]

def lire_releves():
    """Retourne (donnees, source). Source vaut 'postgres' ou 'memoire'."""
    url = os.environ.get("DATABASE_URL")

    if not url:
        return RELEVES_SECOURS, "memoire"

    import psycopg2

    with psycopg2.connect(url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT ville, temperature FROM releves ORDER BY ville"
            )
            lignes = cur.fetchall()

    return [
        {"ville": v, "temperature": t}
        for v, t in lignes
    ], "postgres"


@app.get("/sante")
def sante():
    return jsonify({"statut": "ok", "version": "2"})


@app.get("/releves")
def releves():
    donnees, source = lire_releves()
    return jsonify({
        "source": source,
        "releves": donnees
    })


@app.get("/moyenne")
def moyenne():
    donnees, source = lire_releves()

    if not donnees:
        return jsonify({
            "source": source,
            "moyenne": None
        })

    valeur = sum(
        d["temperature"]
        for d in donnees
    ) / len(donnees)

    return jsonify({
        "source": source,
        "moyenne": round(valeur, 1)
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="0.0.0.0", port=port)
