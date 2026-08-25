releves = [
    {"ville": "Paris", "temperature": 21},
    {"ville": "Lyon", "temperature": 26},
]

def moyenne():
    return sum(r["temperature"] for r in releves) / len(releves)

if __name__ == "__main__":
    print("Temperature moyenne :", moyenne())

releves.append({"ville": "Marseille", "temperature": 27})
