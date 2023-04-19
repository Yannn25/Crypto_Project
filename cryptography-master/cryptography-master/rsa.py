#C.5 RSA
"""
           this file contains just the start function which is just used as a program header
                    The Functions used are present in the  rsa_functions.py  file 
"""


MAX = 20
import random
from time import sleep
import rsa_functions as rsa 
ran =  random.SystemRandom()



def start():
  print(" C5 RSA ")
  print("   please Enter  \n    1 : first Exercise\n    2 : Second Exercise\n    3 : Second Exercise\n    4 : Forth  Exercise\n    5 : Fiveth  Exercise\n   ")
  choice = input("   Exercise  :  ")
  if choice == "1" : 
    print(" \n +++++++++++++++++ Miller Rabin  primilaty test +++++++++++++++ \n  ")  
    value  =  input ("   Enter value : ")
    try :
        value  = int(value)
    except ValueError :
        print("  * Invalid  Enter *   ")
        exit(1)
    
    else : 
       if (value <=6) : 
           print(" * Value too small *")
           exit(1)
       else : 
         print("   *** IMP : The Miller Rabin Test Needs a  Number  \n   <witness>  witch determines the accuracy of the test    *** ")     
         change= input("\n   By Default The Program uses witeness =  800 : would you  change it  <yes> : ")  
         witness = 800
         if (change== "yes") :
             print("\n")             
             try :
                str_witness  = input ("   witness =  ")
                witness =  int(str_witness)
                while witness <= 10 : 
                   str_witness  = input ("  Try With Another Bigger Number =  ")
                   witness =  int(str_witness)
             except  ValueError : 
                 print("  * Invalid  Enter *   ")
                 exit(1)
         if  rsa.miller_rabin (value , witness,ran): 
               print("\n ************************ Is  Prime     *******************************")
         else : 
              print("\n ************************  Is  Not Prime *****************************")     

  elif(choice == "2") : 
      print(" \n +++++++++++++++++ RSA +++++++++++++++ \n  ") 
      genrat = input("   Do You Want To Generate  RSA   Keys  <yes/no> : ")
      if genrat == "yes":
           p = rsa.gen_prime(200,ran)
           q = rsa.gen_prime(100, ran)
           keys =  rsa.generate_key(p,q)
           private_key =  keys[0]
           public_key =  keys[1]
           cipher_exponent = public_key[1]
           n= public_key[0]
           print(" \n   ******** THE KEYS WAS GENERATED SUCCESSFULY**********   \n ")
           print("public_key = ", public_key)
           print("private_key = ", private_key)
           print("N = ", n)

           anser = input("     Do you want to register the keys <yes/no> : ")
           if anser == "yes" : 
              rsa.CreatFIle_and_write("private_key", str(private_key))
              rsa.CreatFIle_and_write("public_key", str(cipher_exponent))
              rsa.CreatFIle_and_write("N", str(n))
              print("\n ***  The Files  (private_key, public_key, N) are Generated *** \n ")
              contin =  input("  \n   Would You  Quit  The Program <no/?> ") 
              if (contin != "no"): 
                print(" \n   ***** GOOD BYE **** ")
                exit(0) 
      elif genrat != "no" : 
           print ("   * ! Wrong   answer  !  * ")   
           exit(1)
             
      choice_2= input (" \n   Would You Crypt Or Decrypt with RSA Algorithm <crypt/dec> : ")
      if (choice_2=="crypt"):
           print(" \n             ***  Encryption With RSA Algorithm   *** \n")
           print (" \n   ***The 'test'file contains a random text chosen radomly from wikipedia (On Quantum physics) could be using as   test file *** \n ")  
           file = input("    1- please filename contient public key : ")
           public_key = int (rsa.ReadFile(file))
           file = input("    2- please filename contient N =q*p : ")
           n = int (rsa.ReadFile(file))
           file = input("    3- please filename contient The text : ")
           text = rsa.ReadFile(file)
           if (len(text) < MAX+4) : 
               print("\n  !! size  text too small  !! ")
               exit(0)
           filename  = "RSAcry_"+file
           file = open(filename, "w")
           rsa.DivisTo_block_and_Crypt(file, text,public_key, n)
           file.close()
           print("\n *** Encryption  Terminated SUCCESSFULY  The  Encrypted file is : ", filename," ***")
      if(choice_2 == "dec") :   
            print(" \n             ***  Decryption With RSA Algorithm   *** \n")
            try :
              file = input("   1- please filename contient private key : ")
              private_key = int (rsa.ReadFile(file))
           
              file = input("   2- please filename contient N =q*p : ")
              n = int (rsa.ReadFile(file))            
            
              file = input("   3- please filename contient The text to Decrypt : ")
              cry_text = rsa.ReadFile(file)
            except ValueError : 
              print("   please make sure that you have entered the right file")
              exit(1)
            else :    
              name  =  "RSAdec_" +  file
              file =  open(name,"w")
              rsa.get_block_and_Decrypt(file, cry_text ,private_key,n)
              file.close()
              print("\n  *** Decryption  Terminated SUCCESSFULY you file Decrypted is : ", name, "***")
  
  elif(choice =="3") :       
       print ("\n      % It's A Text  Formatting Used In Forth Exercise % \n")

  elif (choice == "4") : 
      print (" \n   ***The 'test2 'file contains a random text chosen radomly from wikipedia (On Quantum cryptography ) could be using as   test file *** \n ")  
      print("\n ** To  Use This Hybrid  Encryption plsease Make  Sure You Have \n The RSA Keys (N ,private_key, public_key)  Use sencond question\n if that is necessary ** \n")     
      anser =  input ("   would you  continue  <yes/no> :   ")
      if (anser == "yes") : 
        ans = input ("\n   Do You Want To Encrypt Or Decrypt Please Enter <crypt/dec> :  ")
        if ans == "crypt" : 
           try :
             file = input("\n   1- please filename contient public key : ")
             public_key = int (rsa.ReadFile(file))

             file = input("   2- please filename contient N =q*p : ")
             n = int (rsa.ReadFile(file))

             file = input("   3- please filename contient The text : ")
             text = rsa.ReadFile(file)
             name =  "cryptedAES_"+file
  
             key  = rsa.key_gen()  
             string_key  =  rsa.get_string_key(key)
           except ValueError : 
             print("\n   please make sure that you have entered the right file")
             exit(1)
           else :  
             encrypted_key =rsa.Ecrypt_message (string_key , public_key, n) 
             rsa.CreatFIle_and_write("key",  str(encrypted_key))          

             encrypted_text = rsa.Encrypt_AES_Fun (text,  key) 

             file =  open(name ,  "wb")
             file.write(encrypted_text)
             file.close ()
             print (" *** Encryption  Terminated SUCCESSFULY you file Encrypted is :",name, "***\n  *** The encypted Key : ",  "key  ***")
        
        elif ans == "dec" : 
            try :
               file = input("    1- please filename contient private key  : ")          
               private_key = int (rsa.ReadFile(file))
            
               file = input("    2- please filename contient N =q*p : ")
               n = int (rsa.ReadFile(file))
      
               file = input("    3- please filename contient the Crypted key : ")
               key=  int (rsa.ReadFile(file))

               file = input("    4- please filename contient the Crypted text : ")
               name = file 
               file = open(file , "rb") 
               encrypt_text = file.read()
               file.close()
     
               key = rsa.Decrypt_message (key,  private_key,n)
               key = rsa.get_key_byte_fromstring (key)     
        
               name =  "Decrypt_" +  name

               decrypted_text = rsa.Decrypt_AES_Fun(encrypt_text ,  key )            
               decrypted_text =  rsa.hybrid_jum ( decrypted_text)
               rsa.CreatFIle_and_write (name ,  decrypted_text)
               print (" \n    *** Decryption  Terminated SUCCESSFULY you file Decrypted is :",name , " ***\n    *** The Decypted Key : ",key ," ***")
            except Exception :
               print("\n  please make sure that you have entered the right file")
               exit(1)
        else : 
          print("\n   Unkown  Service  \n") 
      else: 
        print("   ***  See You Again ***  ")  
  elif choice == "5":  
       print ("\n  * Pollard's rho  Factorization algorithm * \n ")
      
       number = input("   Enter a number to factorize : ")
       try :
         number = int(number)

       except ValueError :
         print(" \n  **  Invalid Number  ** \n")  

       else : 
            while True : 
                if (number > (2**57)  or   number < (2**56)) : 
                  print("   The number must be between (2**57) and (2**56)   ")
                  number =  int(input("   Try  again : "))
                else : 
                  break  
             
            def func (x) : 
              return x*x+1 
            fact = (rsa.rho_pollard_factoring (number,  func))
            print  ("facteur =  ( ",   fact," , " ,  number //  fact  ,  " )  " ) 

  print("   ***  Good Bye  ***  ")       
start()




