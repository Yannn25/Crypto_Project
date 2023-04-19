def F(k, x):
    # k est une clé de 16 bits, représentée sous forme d'un entier en base 10
    # x est un bloc de 16 bits, représenté sous forme d'un entier en base 10
    # Les valeurs de k et x doivent être comprises entre 0 et 65535 inclusivement
    
    # Conversion de k en une liste de 16 bits
    key = [(k >> i) & 1 for i in range(16)]
    
    # Conversion de x en une liste de 16 bits
    block = [(x >> i) & 1 for i in range(16)]
    
    # Application de la substitution
    s_box = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8, 0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]
    for i in range(16):
        block[i] = s_box[block[i]]
    
    # Conversion de la liste de bits en un entier
    block = sum([block[i] * 2**(15-i) for i in range(16)])
    
    # Application de la permutation
    perm = [1, 5, 9, 13, 2, 6, 10, 14, 3, 7, 11, 15, 4, 8, 12, 16]
    block_bits = [(block >> (16-i)) & 1 for i in range(1, 17)]
    perm_bits = [block_bits[perm[i]-1] for i in range(16)]
    perm_block = sum([perm_bits[i] * 2**(15-i) for i in range(16)])
    
    return perm_block

def encrypt_ctr(key, nonce, plaintext):
    # key est une clé de 16 bits, représentée sous forme d'un entier en base 10
    # nonce est un nonce de 16 bits, représenté sous forme d'un entier en base 10
    # plaintext est un texte en clair, représenté sous forme d'une chaîne de caractères
    # La longueur de plaintext doit être un multiple de 2
    
    # Séparation de plaintext en blocs de 16 bits
    blocks = [int(plaintext[i:i+2], 16) for i in range(0, len(plaintext), 2)]
    
    # Calcul de la clé pour chaque tour
    keys = [key, ((key << 4) & 0xFFFF) | (key >> 12), ((key << 8) & 0xFFFF) | (key >> 8), ((key << 12) & 0xFFFF) | (key >> 4)]
    
    # Initialisation du compteur
    counter = nonce
    
    # Chiffrement des blocs en utilisant la fonction F en mode compteur
    ciphertext = ''
    for block in blocks:
        # Calcul du bloc chiffré
        encrypted_block = F(keys[counter % 4], counter) ^ block
        
        # Conversion du bloc chiffré en une chaîne de caractères hexadécimaux de longueur 4
        ciphertext_block = hex(encrypted_block)[2:].zfill(4)
        
        # Ajout du bloc chiffré au texte chiffré final
        ciphertext += ciphertext_block
        
        # Incrémentation du compteur
        counter += 1
    
    return ciphertext

def decrypt_ctr(key, nonce, ciphertext):
    # key est une clé de 16 bits, représentée sous forme d'un entier en base 10
    # nonce est un nonce de 16 bits, représenté sous forme d'un entier en base 10
    # ciphertext est un texte chiffré, représenté sous forme d'une chaîne de caractères
    # La longueur de ciphertext doit être un multiple de 4
    
    # Séparation de ciphertext en blocs de 16 bits
    blocks = [int(ciphertext[i:i+4], 16) for i in range(0, len(ciphertext), 4)]
    
    # Calcul de la clé pour chaque tour
    keys = [key, ((key << 4) & 0xFFFF) | (key >> 12), ((key << 8) & 0xFFFF) | (key >> 8), ((key << 12) & 0xFFFF) | (key >> 4)]
    
    # Initialisation du compteur
    counter = nonce
    
    # Déchiffrement des blocs en utilisant la fonction F en mode compteur
    plaintext = ''
    for block in blocks:
        # Calcul du bloc déchiffré
        decrypted_block = F(keys[counter % 4], counter) ^ block
        
        # Conversion du bloc déchiffré en une chaîne de caractères hexadécimaux de longueur 4
        plaintext_block = hex(decrypted_block)[2:].zfill(4)
        
        # Ajout du bloc déchiffré au texte déchiffré final
        plaintext += plaintext_block
        
        # Incrémentation du compteur pour le bloc suivant
        counter += 1
    
    return plaintext

    