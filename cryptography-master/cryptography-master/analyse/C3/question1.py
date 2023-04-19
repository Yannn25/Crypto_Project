import random

def print_doubleByte(varName,value) :
    for i in range (len(value)):
        print(varName + str(i) + " : " + value[i] + " = " + db_to_chr(value [i]))

# Converts a doubleByte into a character
def db_to_chr(db):
    i = 0
    p = 0
    for c in db[::-1] :
        i+= int(c) * (2 ** p)
        p+=1
    return chr(i)

# Couverts a doubleByte into a String of 0 and 1
def to_string(c) :
    s = ""
    if(c == 0) :
        return "00000000"
    while(c > 0):
        s += str(c%2)
        c = c//2
    for i in range (8 - len(s)):
        s+="0"
    return s[::-1]

# Converts a string into an array in doubleByte
def to_doubleByte(x):
    result = [] 
    for elem in x:
        s = ""
        arr = bytearray(elem,"utf-16")
        s += to_string(arr[3]) + to_string(arr[2])
        result.append(s)
    return result

# Calculates a XOR
def xor_db(x,k) :
    result = ""
    for i in range (len(x)):
        result += str((int(x[i]) + int(k[i]))%2)
    return result
            
''' 
    Function that generates a key
    a key is a list [k0,k1,k2,k3]
'''
def G() : 
    L = []
    for i in range (4) : 
        tmp = ""
        for j in range (2) :
            for k in range (8) :
                tmp += str(random.randint(0,1))
        L.append(tmp)
        print(len(tmp))
    return L

'''
    Function that encrypts a message x = [x0,...,xn]
    each xi is coded on 2 bytes
'''
def E(x,k): 
    y = []
    for i in range (len(x)):
        y.append(xor_db(x[i],k[i%4]))
    return y

def E_to_text(e):
    text=""
    for elem in e:
        text+= db_to_chr(elem)
    return text

def D(y,k):
    return E(y,k)
    

'''
    MAIN
'''

def main():
    ## Key Gen
    generated_keys = []
    k = G()

    while (k in generated_keys):
        k = G()

    generated_keys.append(k)
    print("Clé générée :")
    print_doubleByte("k",k)

    while (k in generated_keys):
        k = G()
    generated_keys.append(k)

    ## Encryption
    message = to_doubleByte(input("Message à crypter x : "))
    print_doubleByte("x",message)

    cyphered = E(message,k)
    print("Message crypté y :")
    print_doubleByte("y", cyphered)

    # Decryption
    message = D(cyphered,k)
    print("Message Décrypté : ")
    print_doubleByte("d",message)

main()