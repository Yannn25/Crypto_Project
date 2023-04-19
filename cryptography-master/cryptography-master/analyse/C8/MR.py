import random as rd
from math import *


def max_pui_deux(n):
    if n == 0:
        return 0
    i = 1
    while n % i != 0:
        i *= 2
    return i


'''
    Compute x^n
    Parameters :
    - A number x
    - A power n
'''


def quickExponent(x, n):
    # Base x cases
    if x == 0:
        return 0
    if x == 1:
        return 1
    # Base n cases
    if n == 0:
        return 1
    if n == 1:
        return x
    # Heredity
    if (n % 2 == 0):
        return (quickExponent(x, n//2) ** 2)
    else:
        return (quickExponent(x, n//2) ** 2) * x


'''
    Compute x^n %m
    Parameters :
        - A number x
        - A power n
        - A modulus m
'''


def quickModularExponent(x, n, m):
    # Base x cases
    if x == 0:
        return 0
    if x == 1:
        return 1
    # Base n cases
    if n == 0:
        return 1
    if n == 1:
        return x % m
    # modulo 1 case
    if m == 1:
        return 1
    # Heredity
    if (n % 2 == 0):
        return (quickModularExponent(x, n//2, m) ** 2) % m
    else:
        return ((quickModularExponent(x, n//2, m) ** 2) * x) % m


def miller_rabin(n, k, m):
    if n == 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    # n = 1 + m*2^k, where m is odd,
    # i.e. 2^k is the highest power of 2 dividing n-1, m being the other factor
    a = rd.randint(2, n-1)
    if quickModularExponent(a, m, n) == 1 or quickModularExponent(a, m, n) == n-1:
        return True
    for i in range(1, k):
        if quickModularExponent(a, 2*i*m, n) == n-1:
            return True
    return False


def isProbablyPrime(n, likelihood=99):
    k = max_pui_deux(n-1)
    m = int((n-1)/(quickExponent(2, k)))
    # Base error rate for a single miller-rabin test is about 1/4.
    # So false-positive probability after j tests is 1 - 4^(-j)
    # To reach the given likelihood l, we need 1 - 4^(-j) >= l/100
    # 4^(-j) <= (100-l)/100
    # -j <= log4(100 - l) - log4(100)
    # j >= log4(100) - log4(100 - l)
    # log4(100) is about 3.32, let's round it to 4
    for i in range(floor(4 - log(100 - likelihood, 4))):
        if not miller_rabin(n, k, m):
            return False
    return True


''' 
    TESTS
'''


def main():
    print(quickModularExponent(78, 4567, 154))

    print(miller_rabin(33, 4, 2))  # 33 is 2*2^4 + 1
    print(miller_rabin(31, 1, 15))  # 31 is 15*2^1 + 1
    print(miller_rabin(17, 3, 2))  # 17 is 2*2^3 + 1
    print(miller_rabin(3, 1, 1))  # 3 is 1*2^1 + 1 ???

    print(isProbablyPrime(3))
    print(isProbablyPrime(17))
    print(isProbablyPrime(31))


if __name__ == "__main__":
    main()
