import numpy as np

# Tableau de substitution
S = np.array([0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7])

# Tableau de permutation
P = np.array([0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]) - 1

def F(k):
    """
    Fonction de chiffrement
    
    :param k: clé de chiffrement (entier de 16 bits)
    :return: fonction de chiffrement (216 -> 216)
    """
    # Générer les 4 sous-clés Ki
    k_int = int.from_bytes(bytes(k), byteorder='big')
    K = np.zeros(64, dtype=np.uint8)
    for i in range(4):
        x = np.frombuffer(k_int.to_bytes(2, byteorder='big'), dtype=np.uint8)
        Ki = np.zeros(48, dtype=np.uint8)
        for j in range(48):
            Ki[j] = x[PC2[j] - 1]
        K[i*16:(i+1)*16] = Ki

    def round_function(block):
        """
        Fonction d'un tour
        
        :param block: bloc de 4 bytes à chiffrer
        :return: bloc chiffré de 4 bytes
        """
        # XOR avec la sous-clé
        y = np.frombuffer((block ^ K[i-1]).to_bytes(2, byteorder='big'), dtype=np.uint8)
        
        # Substitution
        s = S[y]
        
        # Permutation
        w = s[P].view(np.uint16)[0]
        
        return w
    
    def Fk(x):
        """
        Fonction de chiffrement
        
        :param x: entier à chiffrer (216 bits)
        :return: entier chiffré (216 bits)
        """
        block1 = (x >> 48) & 0xFFFF
        block2 = (x >> 32) & 0xFFFF
        block3 = (x >> 16) & 0xFFFF
        block4 = x & 0xFFFF
        
        for i in range(1, 5):
            block1, block2, block3, block4 = round_function(block1), round_function(block2), round_function(block3), round_function(block4)
        
        return (block1 << 48) | (block2 << 32) | (block3 << 16) | block4
    
    return Fk


def F_inv(k):
    """
    Fonction de déchiffrement
    
    :param k: clé de chiffrement (entier de 16 bits)
    :return: fonction de déchiffrement (216 -> 216)
    """
    Fk = F(k)
    return lambda x: Fk(x)


k = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

verif = F(k)
expected_output = [12, 14, 1, 9, 14, 3, 3, 13, 2, 3, 3, 2, 7, 9, 9, 8]
print("------ verif -------\n",verif,"\n-------- expcted --------\n",expected_output)
#assert F(k, x) == expected_output

import numpy as np
def xor(a, b):
    """
    Effectue une opération XOR bit à bit entre a et b.
    """
    result = ""
    for i in range(len(a)):
        # XOR bit à bit entre les bits de a et b
        if a[i] == b[i]:
            result += "0"
        else:
            result += "1"
    return result
def hex2bin(s):
    mp = {'0': "0000",
          '1': "0001",
          '2': "0010",
          '3': "0011",
          '4': "0100",
          '5': "0101",
          '6': "0110",
          '7': "0111",
          '8': "1000",
          '9': "1001",
          'A': "1010",
          'B': "1011",
          'C': "1100",
          'D': "1101",
          'E': "1110",
          'F': "1111"}
    bin = ""
    for i in range(len(s)):
        bin = bin + mp[s[i]]
    return bin
substitution_table = {
    '0000': '1110', '0001': '0100', '0010': '1101', '0011': '0001',
    '0100': '0010', '0101': '1111', '0110': '1011', '0111': '1000',
    '1000': '0011', '1001': '1010', '1010': '0110', '1011': '1100',
    '1100': '0101', '1101': '1001', '1110': '0000', '1111': '0111'
}
def substitution(byte):
    binary_value = hex2bin(byte)
    substituted_binary = substitution_table[binary_value]
    return hex(int(substituted_binary, 2))[2:].upper().zfill(2)
def F(k, x):
    # Convertir k et x en binaire
    k_bin = hex2bin(k)
    x_bin = hex2bin(x)
    # Décaler la clé pour chaque tour
    k1_bin = k_bin
    k2_bin = k_bin[4:] + k_bin[:4]
    k3_bin = k_bin[8:] + k_bin[:8]
    k4_bin = k_bin[12:] + k_bin[:12]
    # XOR le bloc d'entrée avec la clé appropriée pour chaque tour
    y1_bin = xor(x_bin, k1_bin)
    y2_bin = xor(x_bin, k2_bin)
    y3_bin = xor(x_bin, k3_bin)
    y4_bin = xor(x_bin, k4_bin)
    # Appliquer la substitution à chaque élément du bloc
    s1_bin = substitution_table(y1_bin)
    s2_bin = substitution_table(y2_bin)
    s3_bin = substitution_table(y3_bin)
    s4_bin = substitution_table(y4_bin)
    # Permuter les éléments du bloc
    p_bin = permutation_table(s1_bin + s2_bin + s3_bin + s4_bin)
    # Convertir le résultat en hexadécimal et le renvoyer
    return bin2hex(p_bin)


def F_inv(k, x):
    sbox = [['E', '4', 'D', '1', '2', 'F', 'B', '8', '3', 'A', '6', 'C', '5', '9', '0', '7']]
    perm_inv = [0, 4, 8, 12, 1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15]
    y = list(x)  # copy input
    for i in range(2):  # 2 rounds
        # permutation inverse
        w = [0] * 16
        for j in range(16):
            w[perm_inv[j]] = y[j]
            
# Test de la fonction F
def test_F():
    # Définir une clé et un bloc d'entrée
    clef = "3F5A"
    bloc_entree = "6FAB"
    
    # Convertir la clé et le bloc d'entrée en binaire
    clef_binaire = hex2bin(clef)
    bloc_entree_binaire = hex2bin(bloc_entree)
    
    # Appliquer la fonction F sur le bloc d'entrée avec la clé donnée
    bloc_sortie_binaire = F(bloc_entree_binaire, clef_binaire)
    
    # Convertir la sortie binaire en hexadécimal
    bloc_sortie_hex = bin2hex(bloc_sortie_binaire)
    
    # Afficher la sortie obtenue
    print("Sortie obtenue : ", bloc_sortie_hex)
    
    # Définir la sortie attendue pour la clé et le bloc d'entrée donnés
    sortie_attendue = "4BFC"
    
    # Vérifier si la sortie obtenue est égale à la sortie attendue
    assert bloc_sortie_hex == sortie_attendue, "Erreur : la sortie obtenue est différente de la sortie attendue"
    
    print("Test réussi !")

# Appeler la fonction de test
test_F()


def encrypt_counter_mode(key, nonce, plaintext):
    """Encrypts plaintext in counter mode using the key and nonce"""
    ciphertext = b""
    counter = 0
    while plaintext:
        # Generate counter block
        counter_block = nonce + counter.to_bytes(8, byteorder='big')
        # Encrypt counter block
        keystream = bytes(F(key, counter_block))
        # XOR with plaintext
        block_size = min(len(plaintext), len(keystream))
        ciphertext += bytes([p ^ k for p, k in zip(plaintext[:block_size], keystream[:block_size])])
        plaintext = plaintext[block_size:]
        counter += 1
    return ciphertext


def decrypt_counter_mode(key, nonce, ciphertext):
    """Decrypts ciphertext in counter mode using the key and nonce"""
    plaintext = b""
    counter = 0
    while ciphertext:
        # Generate counter block
        counter_block = nonce + counter.to_bytes(8, byteorder='big')
        # Encrypt counter block
        keystream = bytes(F(key, counter_block))
        # XOR with ciphertext
        block_size = min(len(ciphertext), len(keystream))
        plaintext += bytes([c ^ k for c, k in zip(ciphertext[:block_size], keystream[:block_size])])
        ciphertext = ciphertext[block_size:]
        counter += 1
    return plaintext
