def getBits(nb):
    if isinstance(nb, bytes):
        nb = int.from_bytes(nb, byteorder='little')
    res = [False]*16
    for i in range(16):
        if nb & (1 << (15 - i)):
            res[i] = True
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

def cutInFour(tab):
    part1 = tab[0:4]
    part2 = tab[4:8]
    part3 = tab[8:12]
    part4 = tab[12:]
    return [part1, part2, part3, part4]

def concat_parts(tab):
    # Note : intended ESPECIALLY to merge 4 4-bits lists into a 16-bit one !!!
    return tab[0] + tab[1] + tab[2] + tab[3]

def C4_sub(n):
    tab = [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7]
    return tab[n]

def C4_Perm(tab):
    res = tab
    perm = [1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15, 4, 8, 12, 16]
    for i in range(16):
        res[i] = tab[perm[i]]
    return res

def getC4Keys(k):
    tab = getBits(k)  # Get bits of the 16-bits key k
    part1 = tab[0:4]
    part2 = tab[4:8]
    part3 = tab[8:12]
    part4 = tab[12:]
    k1 = tab
    k2 = part4 + part1 + part2 + part3
    k3 = part3 + part4 + part1 + part2
    k4 = part2 + part3 + part4 + part1
    return [k1, k2, k3, k4]

def F_helper(k, x):
    keys = getC4Keys(k)
    z = x
    for i in range(4):
        z = xor(z, keys[i])
        z_parts = cutInFour(getBits(z))
        sub_parts = [C4_sub(part) for part in z_parts]
        z = concat_parts(sub_parts)
        z = C4_Perm(z)
        z = bitsToNb(z)
    return z

def F(k):
    return lambda x: F_helper(k, x)


import struct

def encrypt(key, nonce, plaintext):
    counter = 0
    ciphertext = b""
    Fk = F(key)
    plaintext = bytes.fromhex(plaintext)  # convert the hex string to bytes
    while len(plaintext) > 0:
        # generate pseudorandom number
        keystream = Fk((struct.pack("<H", nonce) + struct.pack("<H", counter)))
        # XOR with plaintext to produce ciphertext
        chunk = plaintext[:2]
        plaintext = plaintext[2:]
        ciphertext += bytes([chunk[i] ^ keystream[i] for i in range(2)])
        # increment counter
        counter += 1
    return ciphertext


def decrypt(key, nonce, ciphertext):
    return encrypt(key, nonce, ciphertext) # decryption is the same as encryption in CTR mode


#--------------------------------------------   TESTS   ------------------------------------------------------------
key = 0x3A5C
nonce = 0x7B24
plaintext = '6BC1BEE22E409F96E93D7E117393172A'

ciphertext = encrypt(key, nonce, plaintext)
print(ciphertext)

decrypted_plaintext = decrypt(key, nonce, ciphertext)
print(decrypted_plaintext)

