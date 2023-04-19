from MR import isProbablyPrime, quickModularExponent
from math import gcd
import random

'''
    Global variables for key size
'''
byte_size = 8


'''
    Generates a prime number. Uses Miller-Rabin as primality test.
'''


def generate_prime(size=byte_size):
    r = int.from_bytes(random.randbytes(size), byteorder="little")
    while(not isProbablyPrime(r)):
        r = int.from_bytes(random.randbytes(size), byteorder="little")
    return r


'''
    Finds a number coprime with phi
    Parameters :
        - The value phi = (p-1) * (q-1)

    Returns :
        A number e such as 1 < e < phi(n) and gcd(e,phi(n)) = 1

'''


def find_coprime(phi):
    for i in range(2, phi):
        if (gcd(i, phi) == 1):
            return i
    return -1


'''
    Find the phi modular inverse of e using Euclide's algorithm
    Parameters :
        - The number e
        - The modulo phi
    Returns
        A number d such as ed = 1 mod phi
'''


def find_inverse(e, phi):
    m = phi
    x = 1
    y = 0

    if(phi == 1):
        return 0
    while (e > 1):
        q = e//phi
        t = phi

        phi, e, t = e % phi, t, y
        y, x = x-q*t, t

    if (x < 0):
        x += m
    return x


'''
    Generates public and private keys for RSA

    Returns :
        A list [(n,e),(d,n)] containing the public and the private keys
'''


def generate_RSA(DES=False):
    if (DES):
        p = generate_prime(4)
        q = generate_prime(3)
        while (q == p):
            q = generate_prime()
    else:
        p, q = generate_prime(), generate_prime()
        while (q == p and 2**56 > p*q and p*q > 2**57):
            q = generate_prime()

    n = p*q
    phi = (p-1) * (q-1)
    e = find_coprime(phi)

    d = find_inverse(e, phi)
    return [[n, e], [d, n]]


'''
    Encrypts a message using RSA
    Parameters :
        - msg : the message to encrypt
        - key : the public key (n,e)

    Returns :
        The encrypted message
'''


def encrypt_RSA(msg, key):

    cyphered = quickModularExponent(
        int.from_bytes(bytes(msg, 'UTF-8'), byteorder="little"), key[1], key[0]
    )
    return cyphered


'''
    Decrypt a message using RSA
    Parameters :
        - msg : the message to decrypt in int format
        - key : the private key (d,n)

    Returns :
        The raw message
'''


def decrypt_RSA(msg, key):
    mod = quickModularExponent(msg, key[0], key[1])
    print(mod)
    return mod.to_bytes(64, byteorder="little").decode("utf-8")


'''
    TESTS
'''


def main():
    print("Generated keys : ")
    k = generate_RSA()
    print(k)

    print("Encrypt 'HELLO' :")
    m = encrypt_RSA("HELLO", k[0])
    print("Encrypted message in int format :%d" % m)

    print("Decrypt 'HELLO' : ")
    print(decrypt_RSA(m, k[1]))


if __name__ == "__main__":
    main()
