import random
import time
from math import sqrt

def mod_inv(a, m):
    """
    Calcule l'inverse modulaire de a modulo m à l'aide de l'algorithme d'Euclide étendu.
    """
    t, new_t = 0, 1
    r, new_r = m, a
    while new_r != 0:
        quotient = r // new_r
        t, new_t = new_t, t - quotient * new_t
        r, new_r = new_r, r - quotient * new_r
    if r > 1:
        raise ValueError("a n'est pas inversible modulo m")
    if t < 0:
        t += m
    return t

def log(g, y, p, factors):
    """
    Calcule le logarithme discret en base g modulo p à l'aide de l'algorithme de Pohlig-Hellman.
    factors est la factorisation de p-1 sous forme de liste de paires (qi, ei).
    """
    x = 0
    for q, e in factors:
        # Calcul de gi = g ^ ( (p-1) / qi ) mod p
        gi = pow(g, (p-1) // q, p)
        # Calcul de hi = y ^ ( (p-1) / qi ) mod p
        hi = pow(y, (p-1) // q, p)
        # Calcul de xi = log_gi (hi)
        if gi == 1:
            xi = 0
        else:
            xi = None
            # Résolution récursive du sous-problème
            for j in range(e):
                hj = pow(hi, (q**j), p)
                gj = pow(gi, (q**(e-1-j)), p)
                xj = pow(gj, xi if xi is not None else 1, p)
                xi = j*q**(e-1-j) + xj*mod_inv(hj, p) if xi is not None else xj*mod_inv(hj, p)
        # Calcul de la solution partielle xi' = xi * (qi-1)^i-1
        x += xi * pow(q, (e-1)*x, p-1)
    # Solution du logarithme discret en base g modulo p
    return x % (p-1)


# Fonction pour générer un nombre premier aléatoire de n bits
def generate_prime(n):
    while True:
        p = random.getrandbits(n)
        if is_prime(p):
            return p

# Fonction pour vérifier si un nombre est premier
def is_prime(n):
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i*i <= n:
        if n % i == 0 or n % (i+2) == 0:
            return False
        i += 6
    return True

# Générer un nombre premier p de 512 bits
p = generate_prime(512)
# Trouver un générateur g pour (Zp)*
g = 2
while pow(g, (p-1)//2, p) == 1 or pow(g, (p-1)//3, p) == 1:
    g += 1
# Générer un nombre aléatoire x pour tester la fonction
x = random.randrange(1, p-1)
# Calculer y = g^x mod p
y = pow(g, x, p)
# Calculer le logarithme discret en base g de y modulo p
factors = [(2, 9), (3, 5), (5, 3), (7, 2), (11, 1), (13, 1)]
#start_time = time.time()
result = log(g, y, p, factors)
#end_time = time.time()
print("Résultat du logarithme discret :")# {}".format(result))
#print("Temps de calcul : {:.6f} secondes".format(end_time - start_time))

#Vérifier que le résultat est correct
#assert pow(g, result, p) == y