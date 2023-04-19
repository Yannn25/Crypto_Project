# -*- coding: utf-16 -*-

import random as rd

def formatter(txt):
    # We remove everything but letters, and turn them to uppercase
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

def G():
    return [rd.randint(0, 2**16 - 1), rd.randint(0, 2**16 - 1), rd.randint(0, 2**16 - 1), rd.randint(0, 2**16 - 1)]

def getBits(nb):
    res = [False]*16
    for i in range(16):
        if nb >= 2**(15 - i):
            res[i] = True
            nb -= 2**(15 - i)
    return res

def bitsToNb(bits):
    res = 0
    for i in range(16):
        if bits[i]:
            res += 2**(15 - i)
    return res

def xorBit(x1, x2):
    return (x1 or x2) and not (x1 and x2)

def xor(n1, n2):
    b1 = getBits(n1)
    b2 = getBits(n2)
    bits = [False]*16
    for i in range(16):
        bits[i] = xorBit(b1[i], b2[i])
    return bitsToNb(bits)

def E(msg, key):
    res = ""
    for i in range(len(msg)):
        res += chr(xor(ord(msg[i]), key[i % 4]) % (2**16 - 1))
    return res

def D(msg, key):
    return E(msg, key)

def dictSort(d):
    # Note : sorts a single dict, not a dict array
    # Sort method : sort the items of the dict which are (key, value) tuples
    # using the f : (k, v) -> -v function
    # sorted() method sorts by increasing order, but we want a decreasing order,
    # which is why we put a minus sign
    # then rebuild a dict with this sorted list
    return dict(sorted(d.items(), key=lambda x:(-1)*x[1]))

def tableSort(table):
    # Note : sorts an entire freqTable, i.e. an array of 4 dicts
    return [dictSort(d) for d in table]

def freqTable(msg):
    # key length is 4, we generate one table per key
    table = [dict(), dict(), dict(), dict()]
    occWeight = 4/len(msg) # formally, 4 * 1/len(msg)
    pos = 0
    for i in range(len(msg)):
        key = ord(msg[i])
        if key in table[pos]:
            table[pos][key] += occWeight
        else:
            table[pos][key] = occWeight
        pos = (pos + 1) % 4
    return table

def naive_E_solve(tab):
    # Takes the highest frequency for each integer among k0, k1, k2, k3 and assumes that it maps to an E in plain text
    # Computes the shifting for each integer
    # Returns [k0, k1, k2, k3]
    # TABLE HAS TO BE SORTED
    # E code is 69
    return [xor(list(tab[i].keys())[0], 69) for i in range(4)]

def score3(d, key):
    # E code is 69
    # A code is 65
    # S code is 83
    return d.get(xor(key, 69), 0) + d.get(xor(key, 65), 0) + d.get(xor(key, 83), 0)

def depth3solve(tab):
    # Assumes that the most frequent letter for this table is either E, S, or A and returns the key corresponding to the most likely scenario
    # We assume the key is either the shift needed to go to E, to S, or to A, and we look at the results for the two other letters.
    # The key with the highest frequencies in encrypted text for the three letters summed is kept.
    res = []
    for d in tab:
        Ekey = xor(list(d.keys())[0], 69)
        Akey = xor(list(d.keys())[0], 65)
        Skey = xor(list(d.keys())[0], 83)
        res.append(sorted([(Ekey, score3(d, Ekey)), (Akey, score3(d, Akey)), (Skey, score3(d, Skey))], key=lambda x:x[1])[-1][0])
        # We sort by score and take the last tuple to get the best key, taking its first element gives us the key
    return res

def score6(d, key):
    # E code is 69
    # A code is 65
    # S code is 83
    # T code is 84
    # I code is 73
    # O code is 79
    return d.get(xor(key, 69), 0) + d.get(xor(key, 65), 0) + d.get(xor(key, 83), 0) + d.get(xor(key, 84), 0) + d.get(xor(key, 73), 0) + d.get(xor(key, 79), 0)

def depth6solve(tab):
    # Assumes that the most frequent letter for this table is either E, S, A, T, I, or O and returns the key corresponding to the most likely scenario
    # We assume the key is either the shift needed to go to E, to S, to A, to T, to I, or to O, and we look at the results for the five other letters.
    # The key with the highest frequencies in encrypted text for the six letters summed is kept.
    res = []
    for d in tab:
        Ekey = xor(list(d.keys())[0], 69)
        Akey = xor(list(d.keys())[0], 65)
        Skey = xor(list(d.keys())[0], 83)
        Tkey = xor(list(d.keys())[0], 84)
        Ikey = xor(list(d.keys())[0], 73)
        Okey = xor(list(d.keys())[0], 79)
        res.append(sorted([(Ekey, score6(d, Ekey)), (Akey, score6(d, Akey)), (Skey, score6(d, Skey)), (Tkey, score6(d, Tkey)), (Ikey, score6(d, Ikey)), (Okey, score6(d, Okey))], key=lambda x:x[1])[-1][0])
        # We sort by score and take the last tuple to get the best key, taking its first element gives us the key
    return res

def results(text):

    key = G()
    form_text = formatter(text)
    encr = E(form_text, key)
    freq = freqTable(encr)
    sortedTable = tableSort(freq)
    naiveKey = naive_E_solve(sortedTable)
    key3 = depth3solve(sortedTable)
    key6 = depth6solve(sortedTable)

    print(key)
    print(naiveKey)
    print(key3)
    print(key6)

    #print(form_text)
    #print(encr)

    #print(freq)
    #print(sortedTable)

    print(D(encr, naiveKey))
    print(D(encr, key3))
    print(D(encr, key6))

    print(D(encr, key))

    print()
    print()
    print()


short_text = "Alan Mathison Turing, né le 23 juin 1912 à Londres et mort le 7 juin 1954 à Wilmslow, est un mathématicien et cryptologue britannique, auteur de travaux qui fondent scientifiquement l'informatique."
long_text = "Pour résoudre le problème fondamental de la décidabilité en arithmétiques, il présente en 1936 une expérience de pensée que l'on nommera ensuite machine de Turing et des concepts de programme et de programmation, qui prendront tout leur sens avec la diffusion des ordinateurs, dans la seconde moitié du XXe siècle. Son modèle a contribué à établir la thèse de Church, qui définit le concept mathématique intuitif de fonction calculable.Durant la Seconde Guerre mondiale, il joue un rôle majeur dans la cryptanalyse de la machine Enigma utilisée par les armées allemandes : l'invention de machines usant de procédés électroniques, les bombes1, fera passer le décryptage à plusieurs milliers de messages par jour. Ce travail secret ne sera connu du public que dans les années 1970. Après la guerre, il travaille sur un des tout premiers ordinateurs, puis contribue au débat sur la possibilité de l'intelligence artificielle, en proposant le test de Turing. Vers la fin de sa vie, il s'intéresse à des modèles de morphogenèse du vivant conduisant aux « structures de Turing ».Poursuivi en justice en 1952 pour homosexualité, il choisit, pour éviter la prison, la castration chimique par prise d'œstrogènes. Il est retrouvé mort par empoisonnement au cyanure le 8 juin 1954 dans la chambre de sa maison à Wilmslow. La reine Élisabeth II le reconnaît comme héros de guerre et le gracie à titre posthume en 2013."

results(short_text)
results(long_text)