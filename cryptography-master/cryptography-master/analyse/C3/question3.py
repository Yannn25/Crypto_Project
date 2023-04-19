'''
Réponse question 2:
    On procède par analyse fréquentielle "modulo 4".
    En connaissant la longueur de la clé(4), on fait 4 tables de fréquences selon l'indice du caractère dans le texte.
    On associe alors le caractère le plus fréquent de chaque table avec le caractère le plus fréquent d'une langue
    (Pour l'anglais et le français c'est E)
    On trouve ainsi tous les k[i] et on décrypte le texte en appliquant l'algo de chiffrement (qui sert aussi à déchiffrer) au texte chiffré.

    Une méthode plus élaborée serait de prendre en compte les M lettres les plus fréquentes et essayer de trouver la clé pour chacune de ces lettres,
    puis de conserver la plus probable parmi elles. Pour cela on fait une moyenne de fréquence sur les autres M lettres du top.
    Cela permet de se débarrasser d'un trop fort biais.
'''

### DEBUT DU FICHIER POUR LA QUESTION 3

from random import randint
from question1 import G,E, print_doubleByte, to_doubleByte, xor_db, E_to_text

def read_text(filepath):
    f = open(filepath,"r")
    return f.read()
    
'''
    Turns every letters in Uppercase, without accent.
    Removes all spaces and punctuation.
'''
def formatter(txt):
    # Uppercase letters have ascii codes from 65 (A) to 90 (Z) included
    # Lowercase letters go from 97 (a) to 122 (z)
    # Mapping to uppercase is just subtracting 32.
    res = ""
    for i in txt:
        if 65 <= ord(i) <= 90:
            res += i
        elif 97 <= ord(i) <= 122:
            res += chr(ord(i) - 32)
        elif i in "àäâÀÄÂ":
            res += "A"
        elif i in "çÇ":
            res += "C"
        elif i in "éèëêÉÈËÊ":
            res += "E"
        elif i in "ïîÏÎ":
            res += "I"
        elif i in "öôÖÔ":
            res += "O"
        elif i in "ùüûÙÜÛ":
            res += "U"
    return res

## Build a frequency table from a text
def freqTables(txt):
    table = [dict(), dict(), dict(), dict()]
    for i in range (len(txt)):
        if(i%4 == 0):
            add_to_dict(table[0], txt[i])
        elif (i%4 == 1):
            add_to_dict(table[1], txt[i])
        elif (i%4 == 2):
            add_to_dict(table[2], txt[i])
        elif (i%4 == 3):
            add_to_dict(table[3], txt[i])
    for i in range (len(table)):
        table[i] = sort_dict(table[i])
    return table

## Add a character as a key to dict : if the key already exists, increment the value
def add_to_dict(d,c):
    if c in d:
        d[c] += 1
    else:
        d[c] = 0

## Returns a sorted dictionary
def sort_dict(d):
    return dict(sorted(d.items(),key=lambda item:item[1], reverse = True))

'''
    From the frequency table, we assume that the most frequent letter is 'E'
    With this information, we crack the key
'''
def crack_key(table):
    k = []
    for i in range (len(table)):
        # Get the most frequent letter
        letter = next(iter(table[i]))
        letter = to_doubleByte(letter)
        x = xor_db(letter[0],to_doubleByte("E")[0])

        k.append(x)
    return k

def decrypt(c):
    return

## Applying our algorithm on a long text
def q3_long(l,nbtest):
    postest = 0
    T = read_text("./longText.txt")
    for i in range (nbtest):
        k = G()
        r = randint(0,T-l)
        t = T[r:r+l]
        c = E(t,k)
        d = decrypt(c)
        if (d == t):
            postest+=1
    if(postest>= nbtest//2):
        q3_long(l//2,nbtest)
    else :
        return l

k = G()
text = to_doubleByte(formatter(read_text("longText.txt")))
e = E_to_text(E(text,k))
tables = freqTables(e)
print("Frequencies :")
print(tables)
print("Cracked key:")
print_doubleByte("k",crack_key(tables))