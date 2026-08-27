from app import app


def test_sante_repond_ok():
    client = app.test_client()
    reponse = client.get("/sante")
    assert reponse.status_code == 200
    assert reponse.get_json()["statut"] == "ok"


def test_moyenne_sans_base():
    client = app.test_client()
    donnees = client.get("/moyenne").get_json()
    assert donnees["source"] == "memoire"
    assert donnees["moyenne"] == 24.0
