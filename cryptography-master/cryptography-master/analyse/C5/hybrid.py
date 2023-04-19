from random import randbytes
from math import gcd
from RSA import *
from MR import quickModularExponent
from Crypto.Cipher import AES
'''
    Bit stuffs a text in order to make its length a multiple of 16
    Parameter :
        - The raw text
    Returns :
        The bit stuffed raw text
        (For unknown reasons, modifying the text without returning it results in an unchanged text)
'''


def stuffing(rawtext):
    if len(rawtext) == 16:
        rawtext += 16*chr(16)
    else:
        r = len(rawtext) % 16
        r = 16-r
        rawtext += (r)*chr(r)
    return rawtext


'''
    Hybrid text encryption function using AES and RSA
    Parameters :
        - The raw text
        - The public key generated by RSA
    Returns :
        The cyphered text
'''


def encrypt_hybrid_AES(text, rsa_pubkey):

    # 16 hardcoded because it's AES
    k = randbytes(16)
    cyphered_key = encrypt_RSA(str(k), rsa_pubkey)

    aes = AES.new(k)
    text = stuffing(text)
    cyphered_message = int.from_bytes(
        aes.encrypt(text.encode()), byteorder="little")

    return cyphered_key, cyphered_message


'''
    Pollard's factorisation function
    WARNING : This function can make the program run in an endless loop
    Parameters :
        - A number n
    Retuns :
        p,q two prime numbers such as n = pq
'''


def pollard(n):
    f = lambda x : x**2 + 1
    x, y, d = 2, 2, 1
    while d == 1:
        x = f(x) % n
        y = f(f(x)) % n
        d = gcd(x-y, n)
    return d, n//d


'''
    Supposing that :
        - we use DES functions with a key on 56 bits
        - 2**56<= n=pq <=2**57
        - we have the public key (n,e)
    Crack the key

    Parameters:
        - The encrypted key
        - The public key generated by RSA

    Returns :
        The decrypted key
'''


def decrypt_DES(des_key, pub_key):
    p, q = pollard(pub_key[0])
    phi = (p-1)(q-1)

    d = find_inverse(pub_key[1], phi)

    return decrypt_RSA(des_key, (pub_key[0], d))


'''
    TESTS
'''


def main():

    # Testing hybrid encryption
    print("Hybrid Encrypting 'HELLO' : ")
    k = generate_RSA()
    key, message = encrypt_hybrid_AES("HELLO", k[0])
    print("Encrypted AES key = ", key)
    print("Encrypted message in int format = ", message)

    # Testing DES
    des_key = randbytes(7)
    encrypted_key = encrypt_RSA(str(des_key), k[0])
    print("Encrypted DES key = ", encrypted_key)
    print("Decrypted DES key = ", decrypt_DES(encrypted_key, k[0]))

    return


if __name__ == "__main__":
    main()