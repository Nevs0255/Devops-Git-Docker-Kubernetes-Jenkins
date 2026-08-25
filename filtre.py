from app import releves

def par_ville(nom):
    """Retourne les releves d'une ville. Liste vide si la ville est inconnue."""
    return [r for r in releves if r["ville"].lower() == nom.lower()]

if __name__ == "__main__":
    print(par_ville("Lyon"))
    print(par_ville("Ville-Inconnue"))
