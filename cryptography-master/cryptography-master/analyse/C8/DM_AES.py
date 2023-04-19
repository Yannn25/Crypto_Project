# -*- coding: utf-16 -*-

from Crypto.Cipher import AES
from RSA import generate_RSA
from MR import quickModularExponent


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


def cutInFour(tab):
    part1 = tab[0:4]
    part2 = tab[4:8]
    part3 = tab[8:12]
    part4 = tab[12:]
    return [part1, part2, part3, part4]


def concat_parts(tab):
    # Note : intended ESPECIALLY to merge 4 4-bits lists into a 16-bit one !!!
    return tab[0] + tab[1] + tab[2] + tab[3]


'''
    C4 substitution function. Maps integers from 0 to 15 to another.
'''


def C4_sub(n):
    tab = [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7]
    return tab[n]


'''
    C4 permutation function. Swaps bits within a single 16-bit block.
'''


def C4_Perm(tab):
    res = tab
    perm = [1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15, 4, 8, 12, 16]
    for i in range(16):
        res[i] = tab[perm[i]]
    return res


'''
    C4 key computation function. Creates four 4-bits keys with the 16-bits key k.
'''


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


def F(k, x):
    keys = getC4Keys(k)
    z = x
    for i in range(4):
        z = xor(x, keys[i])  #  XOR with the key
        z_parts = cutInFour(getBits(z))
        sub_parts = [C4_sub(part) for part in z_parts]  # Substitution
        z = concat_parts(sub_parts)
        z = C4_Perm(z)  # Permutation
        z = bitsToNb(z)
    return z


def F(k):
    return lambda x: F(k, x)


'''
    Davies-Meyer's compressing function
'''


def davies_meyer(B, H):
    aes = AES.new(B)  # Encryption using B as the key...
    return aes.encrypt(H) ^ H  # And H as the message, to then be xored.


init_value = 0

init_vector = init_value.to_bytes(16, 'little')  # Little endian

'''
    Merkle_Damguard's Hashing function
'''


def hash_merkle_damguard(text):
    # We work with blocks of length 16 due to AES
    # text length is based on ASCII length which is 8 bits a char, but here we pas on 16-bits chars. Hopefully we declared an utf-16 encoding on line 1.
    nb_blocks = len(text)
    # No padding is required here since "text" is actual text, following utf-16 encoding as asked, and therefore perfeclty valid blockwise.
    H_i = init_vector
    for i in range(nb_blocks):
        H_i_plus_1 = davies_meyer(text[i], H_i)
        H_i = H_i_plus_1
    return H_i


'''
    Signature using hashing
'''


def sign_RSA(text):
    keys = generate_RSA()
    cyphered = hash_merkle_damguard(text)

    # keys[1] = (d,n)
    signature = quickModularExponent(int(cyphered), keys[1][0], keys[1][1])
    return signature


'''
    Signature verification
    Parameters :
        - The cyphered text 
        - The signature sign
        - The public key pub_key = (n,e) from RSA
'''


def verify_RSA(text, sign, pub_key):
    return hash_merkle_damguard(text) == quickModularExponent(sign, pub_key[1], pub_key[0])


'''
    TESTS
'''


def main():
    # TODO
    return


if __name__ == "__main__":
    main()
