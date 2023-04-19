import Crypto.Cipher.AES as AES
import os 
import  rsa_functions   as rsa



#return 16 bytes of 0  as vector
def get_vector () : 
    IV =B'\0'
    for i  in range (15) : 
        IV+= b'\0'
    return   IV


def Davies_Meyer  ( first_block  ,  second_block ) :
    #take the second block as key of the AES crypt function 
     key  =  second_block 
     iv=  get_vector()

     #code the first block using the second block as a key
     cipher = AES.new(key, AES.MODE_CBC,  iv)
     dec = cipher.encrypt(first_block) 
     
     #apply the xor function between the  encoding result  and the second block 
     result =bytearray(b'') 
     for i  in range(len(second_block)) : 
            res = (dec[i] ^ second_block[i])
            result.append(res)


     rest = b''
     rest =  bytes(result)
     return rest

def add_padding (string): 
    string =  bytes(string , 'utf_8')
    while len(string) != 16 : 
        string = b'0'+string
    return string   



"""
the function takes the text and add the paddind described in  C5 to get blocks_number %16 == 0 
split result into 16 byte block  ,  add the last passing witch is the  binary representation 
of blocks number
"""
def get_block(text) :  
    #add padding to get nb%16==0  blocks
    text =  rsa.complete_text (text)
    list_block  = [] 
    block=b''
    for lettre in text  : 
       byte_block  =  bytes (lettre  , 'utf-8')
       if len(block)   == 16 : 
           list_block.append(block)
           block  =  byte_block   
       else : 
          block += byte_block    
    list_block.append(block)

    size  =  len( list_block ) 
    size    =  str (bin (size) )   
    size =  size[2:]   
    #add a last padding for the last block which contain binary representation of blocks number 
    list_block .append (add_padding (size) )  
    return  list_block



def  Merkle_Damgard (text)  : 
    #get vector
    IV=get_vector()
    blocks =  get_block(text) 
    init_key =  IV 

    #code the first block with the vector "0...0" and  Davies_Meyer function 
    result =  init_key 

    #for all  blocks , take the result of last coding  and use it as key to  code the next block 
    #the first block will be coded with the initial vector 
    for block in  blocks :
       result = Davies_Meyer(block ,  result)         

    return result  
    

#crypt the message 
def sign (message ,  public_key ,n): 
    file =  open("signed_message", "w")
    rsa.DivisTo_block_and_Crypt(file, message,public_key, n)
    file.close()



#starting  function  
def  start ()  :  
   print(" C:8 Compression and Hash   ")
   print( "    please Enter :\n      1-Davies_Meyer\n      2-Merkle_Damgard \n      3-Message signing")
   anser =  input("    choice :  ")
   if anser == "1" :   
     first_block=os.urandom(16)
     second_block=os.urandom(16)
     print("\n *", Davies_Meyer(first_block , second_block), "* \n")
     print(" \n\n The The 2 Two Blocks Used Are blocks of 16 bytes  Randomly Generated \n  go to the start function to change it explicitly")
   
   elif anser == "2" : 
    test ="ceci est un test pour la fonction de hahage en suivant la construction de Merkle_Damgard"      
    print(Merkle_Damgard(test))
    print(" \n\n The text chosen is (", test,  ")\n  go to the start function to change it explicitly")
   
   elif anser =="3" : 
    print (" \n   ***The 'test'file contains a random text chosen radomly from wikipedia (On Quantum physics) could be using as   test file *** \n ")   
    print("\n ** To  Use message signing plsease Make  Sure You Have \n The RSA Keys (N ,private_key, public_key)  Use sencond question from  rsa.py \n if that is necessary ** \n")     
    ans=input("Would you  Sign or  check  the message signature  : <sign/ check > ")  
    if ans== "sign":
       file = input("\n   1- please filename contient public key : ")
       public_key = int (rsa.ReadFile(file))

       file = input("   2- please filename contient N =q*p : ")
       n = int (rsa.ReadFile(file))       

       file = input("   2- please filename contient The message to sign  : ")
       message =  (rsa.ReadFile(file))     
       if (len(message) < 24) :
           print("message length too small")
           exit(1)  

       sign (message ,  public_key ,n)
       print("   The file signed Generated SUCCESSFULY  'signed_message '" ) 


    elif ans=="check" :
       try :   
         file = input("\n   1- please filename contient private key : ")
         private_key = int (rsa.ReadFile(file))

         file = input("   2- please filename contient N =q*p : ")
         n = int (rsa.ReadFile(file))       

         file = input("   2- please filename contient The  signed message   : ")
         signed_message =  (rsa.ReadFile(file))       
       
         file = input("   2- please filename contient The message  : ")
         message =  (rsa.ReadFile(file))       
       except ValueError :
          print("   please make sure that you have entered the right file")
          exit(1)
       else : 
         name  =  "Decrypt_message" 
         file =  open(name,"w")
         rsa.get_block_and_Decrypt(file, signed_message ,private_key,n)
         file.close()
         text =  rsa.ReadFile (name)     
         if (text == message) : 
           print("   \n*The message is correctly identified* ")
         else : 
           print("   \n *The message is not identified* ")    

   else : 
       print("     \n******Unknow Service *********\n ")
start()




