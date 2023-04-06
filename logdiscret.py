# algo naif, si aucune valeur de x ne satisfait l'équation alors boulce infini
def naif(g, y, p):
    x = 1
    gx = g
    while gx != y:
        x += 1
        gx = (gx * g) % p
    return x




