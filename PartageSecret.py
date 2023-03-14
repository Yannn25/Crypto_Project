import random
from sympy import nextprime

def generate(m, k):
    # Trouver un nombre premier p adapté
    p = nextprime(m)

    # Définir les coefficients du polynôme
    a = [random.randint(1, p-1) for i in range(k)]
    a.insert(0, 0)

    return p, a

def distribute(m, k, p, a, s):
    assert k+1 <= len(a), "Erreur : le nombre de coefficients doit être supérieur ou égal au seuil de sécurité k"
    # Définir les parts de secret pour chaque agent
    parts = []
    for i in range(1, m+1):
        xi = random.randint(1, p-1)
        pi = sum(a[j]*xi**j for j in range(k+1)) % p
        si = (s + pi) % p
        #print(f"Agent {i}: xi={xi}, pi={pi}, si={si}")
        parts.append(si)

    return parts

def coalition(p, k, shares):
    # vérification de la taille de shares
    if len(shares) < k+1:
        print("Erreur: pas assez de parts pour reconstruire le secret.")
        return None 
    # récupération de la liste des indices i et des parts de secret si
    indices = [share[0] for share in shares]
    secrets = [share[1] for share in shares]
    # initialisation des variables
    s = 0
    numerator = 1
    denominator = 1
    
    # calcul de la somme pondérée des secrets
    for i in range(len(secrets)):
        # calcul de la fraction partielle
        numerator *= -indices[i] % p
        denominator *= (indices[i] - indices[(i+1)%len(indices)]) % p
        s += secrets[i] * numerator * pow(denominator, -1, p) % p
    
    # renvoi du secret
    return s % p




# Définir les paramètres
m = 9
k = 2
secret = 3
print("Secret de base : ",secret)

# Générer le nombre premier p et les coefficients du polynôme
p, coeffs = generate(m, k)

print("val de p :",p)
print("val de coeffs :",coeffs)

# Distribuer les parts de secret aux agents
parts = distribute(m, k, p ,coeffs, secret)
print("Parts : ",parts)

# Simuler une coalition de k+1 agents et récupérer leurs parts
coalition_parts = [(i+1, parts[i]) for i in range(len(parts))]
print("part des coalition : ", coalition_parts)

# Récupérer le secret en utilisant la fonction coalition
recovered_secret = coalition(p, k, coalition_parts)

print("Secret de base : ",secret," , le secret récuperer : ",recovered_secret)