

#cryptography

C1 : vernam faible 
    The Vernam cipher is a Vigenère cipher, but with an encryption key which must have the same number of letters or even greater than the number of characters in the plain message, in this example we have taken by convention that the size of the key is 4 bytes

C3 : RSA 
  RSA is a public-key cryptosystem that is widely used for secure data transmission. It is also one of the oldest. The acronym "RSA" comes from the surnames of Ron Rivest, Adi Shamir and Leonard Adleman, who publicly described the algorithm in 1977    


-------------------------------------#  The Programm Use #---------------------------------------


Each file codes a section of the project  : 
 vernam.py : for C1 <vername faible >
 rsa.py    ; for C5 < RSA >
 hash.py   : for c8 <COMPRESSION ET HASHAGE>


vernam.py 

as soon as the program  is launched ,  must choose the desired option either crypt or decrypted    
       Important to know : 
           if the decrypt option has been chosen, No special character must be present in the original  
           file <use dedicated option if necessary>  

rsa.py 
as soon as the program is  launched ,  must choose the desired option according  to  the 
       possibilities indicated     
       - Important to know : All informations about encryption and decryption  must be in file 
         (binary or text ), the generated files by rsa are well-named text files
          <samll  changes can lead to encryptions/decryptions errors>

hash.py 
all the instructions are indicated after  the program launching 
