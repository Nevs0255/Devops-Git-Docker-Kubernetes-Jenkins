from app import releves

def par_ville(nom):
    return [r for r in releves if r["ville"].lower() == nom.lower()]

if __name__ == "__main__":
    print(par_ville("Lyon"))
