from filtre import par_ville

def moyenne_ville(nom):
    lignes = par_ville(nom)
    if not lignes:
        return None
    return sum(r["temperature"] for r in lignes) / len(lignes)
