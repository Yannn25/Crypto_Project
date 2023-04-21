from math import ceil, sqrt
import time
def log_naif(g, y, p):

    l=[]
    for x in range(p):
        l.append(pow(g, x, p))

    for x in range(len(l)):
        if y == l[x]:
            
            return x
    return None


#algo bsgs 
def algo(g, y, p):
    t = int(ceil(sqrt(p)))
    table = {pow(g, j, p):j for j in range(t)}
    r = pow(g, -t, p)
    
    for i in range(t):    
        h = (y * pow(r, i, p)) % p
        if h in table:
            return i*t + table[h]
    return None

        
        
y=11
g=3
p=54779

start_time = time.time()
x = algo(g, y, p)
end_time = time.time()

if x is not None:
    print(f"Le logarithme discret de {y} en base {g} modulo {p} est {x}")
else:
    print("Aucune solution trouvée")
print("Temps d'exécution:", end_time - start_time, "secondes")


start_time1 = time.time()
y = log_naif(g, y, p)
end_time1 = time.time()

if x is not None:
    print(f"Le logarithme discret de {y} en base {g} modulo {p} est {x}")
else:
    print("Aucune solution trouvée")
print("Temps d'exécution:", end_time1 - start_time1, "secondes")


