from  random import randint
from time import sleep
import Crypto.Cipher.AES as AES
import codecs
import os 
MAX = 20 



#Firt Exercise
"""
miller rabin primality test
  * Algorithm * 
Input #1: n > 3, an odd integer to be tested for primality
Input #2: k, the number of rounds of testing to perform
Output: “composite” if n is found to be composite, “probably prime” otherwise
"""
#algorithm seen/presented in class 
def witness_miller (number, a):  
    exp = number-1
    #while exp  is  event get the odd exp 
    while  not exp & 1: 
        exp >>=1
    
    if  pow(a , exp , number ) == 1 : 
        return True

#check  if  (a(n-1/2)or.........or a(n-1/2k)+1) equal to negative 1 mod n , if true that meaing n is composite
    while exp  < number - 1 : 
        if pow(a ,  exp , number) == number - 1 : 
            return  True 

        exp <<=1

    return False 


#miller_rabin test,  choose a witness and test randomly 
def miller_rabin (n , k, ran_system): 
    for i  in range (k): 
        # choose randomly a number like (witness-miller)  from  the testing 
        a=ran_system.randrange(2,n-1)
        if  not witness_miller (n, a): 
            return False
    # return True if  all the tests are passed        
    return True   



def pgcd (a ,b) : 
   if  b==0 : 
      return a 
   else : 
      r=a%b
      return pgcd(b,r)


#Extended Euclidean algorithm  from wikipia
def  extended_Euclidean (a,b) : 
    r,u ,v,qr,qu,qv= a,1,0,b,0,1
    while (qr !=0):
     q=r//qr
     r,u ,v,qr,qu,qv = qr, qu,qv,(r-q*qr),u-q*qu,v-q*qv    
    return v 


"""
generate RSA keys by choosing a random number witch is 
the cipher exponent such that gcd (pi , cipher exponent) = 1 
get decryption exponent with using extended Euclidean
"""
def generate_key(p, q):
   n=p*q
   pi=(p-1)*(q-1)
   cipher_exponent =  randint(2,pi-1)    
   while (pgcd(pi,cipher_exponent)!=1 ):
       cipher_exponent =  randint(2,pi-1)
   decryption_exponent = extended_Euclidean (pi,cipher_exponent)  
   private_key=decryption_exponent
   public_key = (n,cipher_exponent)
   return(private_key,public_key )




#random numbers generation
def  gen_prime (size,ran_system) :
    prime_number = 10**size
    begin = 10**size
    limit = 10**(size+1)
    while  not miller_rabin (prime_number , 900,  ran_system) : 
         prime_number=ran_system.randrange(begin, limit)
    return prime_number     
       

def CreatFIle_and_write (namefile , text ):
    file  =  open(namefile ,  "w") 
    file.write(text)
    file.close()


def ReadFile (filename): 
    try  :
     file = open(filename, "r")
    except : 
        print(" No such  File ")
        exit(1)
    else :
       text = file.read()
       file.close()
       return text      



"""
  -- Encrtption --
  take each letter of the text get its ascii code , add zeros at beginning to keep the same lenght 
  apply the RSA algorithm ,  return the result  

"""

def Ecrypt_message (message , public_key, n): 
    liste =[]
    for lettre in message : 
       char =  str(ord(lettre))  
       while (len(char)< 4): 
           char = "0"+char 
       liste.append(char)

    digit_message = ""
    for elem in liste : 
        digit_message = digit_message + elem  
    
    digit_message =  int(digit_message)
    encrypt_message = pow(digit_message, public_key, n)
    return encrypt_message


"""
split the   plain text  into blocks of MAX size 
encrypt the block and add a termination mark  witch is '\n'
repeat the operation while there is block  to  crypt 
"""

def DivisTo_block_and_Crypt(file, text,public_key, n) : 
   block =  ""
   for  lettre  in  text: 
       if  len (block) == MAX:   
           msg = Ecrypt_message (block , public_key, n)
           file.write(str(msg))
           file.write("\n")
           block =  lettre 
       else : 
           block  =  block   +  lettre  
   if (len(block) > 0): 
       msg = Ecrypt_message (block , public_key, n)
       file.write(str(msg))
   

"""---  Decryption --- 
 take the message (as a number sequence) cast and apply the RSA algorithm for decryption
 if the encrypted message size % 4 != 0 this means that the first zeros are lost after the first 
 caste (Encryption), split the encrypted text into 4 byte block , get the char of each block 
 by concatenating the result
"""



def Decrypt_message (message,  private_key,n):  
    message = int(message)
    message =  pow(message,private_key, n)
    message =  str(message)
    if len(message)%4 == 1 : 
        message = "000" +  message
    elif len(message)%4 == 2 : 
        message = "00" + message
    elif len(message)%4 == 3:         
        message = "0" + message
    else : 
        message = message
    
    lettre = ""
    sentence  = ""
    for digit  in message : 
        if  len(lettre) == 4 : 
            sentence  = sentence  +  chr (int(lettre))
            lettre  =  digit
        else : 
            lettre =  lettre  +  digit 
    sentence  = sentence  +  chr (int(lettre))
    return(sentence)



#go through eatch  block  and decrypt it 
def get_block_and_Decrypt(file,text,private_key,n):
    blocks = text.split()
    for  message in  blocks :
       msg =  Decrypt_message (message,  private_key,n)
       file.write(msg)





#padding of the 4th question
def complete_text (message): 
    size =  len(message)
    rest  = size%16
    if  rest==0 : 
       for i  in  range (16): 
           message  = message + chr(16)
    
    else :  
       pi =  16-rest
       for i in range (pi): 
         message = message +  chr(pi)
    return message 




#clean the hybrid 
def  hybrid_jum ( string  ): 
  hybrid_num  =  ord (string [len(string)-1])
  return string[0:(len(string) - hybrid_num)]
    






#generate keys of size 16 bytes using ascii encoding 
def key_gen (): 
    while True :
      try:
          key = os.urandom(16) 
          st =  key.decode("ascii")
      except UnicodeDecodeError :
       pass 
      else : 
         return key 



#convert key from bytes to character
def get_string_key (key) : 
    key_asString  =""
    for i in range (len(key)) : 
     key_asString =  key_asString + chr(key[i])
    return  key_asString      
        


   
#encryption  with using AES python  function 
def Encrypt_AES_Fun (text,  key) :
    try : 
       iv = key 
       text   =  complete_text(text)
       text =  text.encode ('utf-8')
       cipher = AES.new(key, AES.MODE_EAX,  iv )
       dec = cipher.encrypt(text) 
    except Exception : 
       print(" \n *The program uses an utf-8 encode* \n *The characters above must not be present*")
       exit(1)
    return  dec


    

#convert  the key from  byte to string  using ascii  encoding 
def get_key_byte_fromstring (key_asString ) : 
    let =  b''
    for  lettre  in  key_asString : 
         st = (chr(ord(lettre)))
         char =  bytes(st, 'ascii')
         let =  let +  char 

    return  let   






#decryption with using the AES python function 
def Decrypt_AES_Fun(text ,  key ): 
    iv =  key 
    cipher =  AES.new (key, AES.MODE_EAX,  iv)
    dec =  cipher.decrypt(text)
    return  str (dec , 'utf-8')  







# roh pollart factoring implementation 
""" algorithm seen in class """
def rho_pollard_factoring (n,  fun ): 
    x, y, d = 2, 2, 1
    while d==1:
        x = fun(x) % n  
        y = fun(fun(y)) % n
        d = pgcd(x-y, n)
    return d

