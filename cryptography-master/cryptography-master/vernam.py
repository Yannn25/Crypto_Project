# C3 VERNAM FAIBLE 
# all C3 exercises are included in this file
"""
The Vernam cipher is a Vigenère cipher, but with an encryption key which must have the same number of letters or even greater than the number of characters in the plain message, in this example we have taken by convention that the size of the key is 4 bytes
"""
from random import choices, randrange
from re import L
import string
from time import sleep

lettre = ['e','a','i',' ','s' , 'n'] 

# this Function choose randomly  a number between 33,126 and return its equivalent as char (ascii table)
def get_ran_char() : 
  char = randrange(33,126)
  return  chr(char)     

#generate a key of given size 
def get_key (size=None) : 
  if size == None : size=4     
  key=""
  for i in range(size): 
     key=key+get_ran_char()
  return key     



#encrypt the message using XOR function 
def chiffrer (message, key):
  size_key= len(key)
  message_crypt=""
  for  i  in range(len(message)): 
     var = (ord(message[i]) ^ ord(key[i%size_key]))
     message_crypt = message_crypt + chr(var)
  return message_crypt   


"""
 Exo2 : Annalyse 
"""

#the function takes all the text and cut it into blocks of 4 bytes , and return the list of blocks
def get_list_token (text): 
   list_token= []
   word = text[0]
   for i in range(1,len(text)): 
       if i%4 == 0: 
        list_token.append(word)
        word=""
        word = word + text[i]   
       else:
        word= word+text[i]

   
   return list_token

#return the most repeated characters  in list of block
def most_repet_char (list_char) : 
  max = ['', 0]
  for i in  range (len(list_char)): 
      if ( list_char .count(list_char[i])> max[1]): 
          max[0]= list_char[i]
          max[1]=list_char.count(list_char[i])

  return max[0]  



#returns the list of characters that matches position (pos) 
def get_list_char (list_words, pos):
  list_char = []
  if (pos > 3) : return list_char
  for i in range (len(list_words)): 
     list_char.append(list_words[i][pos])
  return list_char       


#returns the list of possible characters 
#using frequency analysis with the first 6 most repeated characters in French
def getkeychar (list_char) : 
   char_repeted = most_repet_char(list_char)
   key_char = ""
   keys =  []
   for pos  in range (4) : 
     key_char=  lettre[pos]
     for i  in range (255) : 
       if ( chr(i ^ ord(key_char) ) == char_repeted) :  
               keys.append(chr(i))    
   return keys



#define the possible characters of the plain text
alphabet = list(string.ascii_lowercase)
alphabet.append(' ')
alphabet.append(chr(10))

"""
the previous function returns a list of possible characters
that may encode the most repeated letter ,but also it must 
code the other letter of the same block,knowing that the plain 
text is an (alphabet)  sequence so  we delete the keys that do not 
give the right letters
"""
def test_key(list_char, list_charkey): 
   li = []
   for j in range(len(list_charkey)) : 
       cmp = 0
       for i  in range ( len(list_char)):
          char = chr(ord(list_charkey[j]) ^ ord(list_char[i]))
          if (char in  alphabet) : 
                 cmp = cmp +1
                     
       if (cmp == len(list_char)) :      
           li.append(list_charkey[j])

   return li         



#decrypt the message 
def crypt_analyse (text): 
  list = []
  list_bloc  = get_list_token(text)
  for pos in range (4) : 
    li_char = get_list_char(list_bloc,pos)
    li =  getkeychar (li_char)
    list.append( test_key(li_char,li))
  return list

#print all the possiblities 
def get_key_pro (list) : 
   morzero =  False
   lesszero = False   
   for pos in range (4) : 
     if (len(list[pos]) >0 ):
         morzero = True 
     if (len(list[pos])<=0):
         lesszero = True 
     if (morzero == True and lesszero == True): 
       print(" * Erroneous decryption : special characters maybe present in your clear text,please be sure to clean up the text *\n  - Use option decrypt with cleaning text ")    
       break 
   for i in range(len(list[0] )): 
     for j in range(len(list[1])): 
       for k in range(len(list[2])): 
         for l  in range(len(list[3])) : 
            key = list[0][i] + list[1][0] + list[2][k] + list[3][l]
            print(" ",key ," ascii ordre : " , ord(list[0][i])," " ,ord (list[1][0])," ",ord(list[2][k]) ," ",ord(list[3][l]))  



#clean a text
def  clean_text (text) : 
  new_text= ""
  for i in range(len(text)): 
     if (text[i] == "à"): 
          new_text=new_text + "a"
     if (text[i] == "é" or text[i] =="è"): 
         new_text=new_text + "e"
     if (text[i] in alphabet ):
         new_text=new_text + text[i]
     

  return new_text



#starting  programme function  
def start () : 
  print("  Please Entrer <crypt> To Encrypt  <dec > : To  Decrypt ")
  choice =  input(" your choice : ")
  if (choice == "crypt") : 
     print("\n------------------------------Encryption--------------------------------------------\n")
     clean = input (" Do you want to use Clean Text option to clean special characters  yes\\no :  ")
     if (clean !="yes") :  
           if (clean !="no"):
              print(" wrong anser ! ")
              exit(1)
     print(" To encrypt enter the  file path to be encrypted : ")
     file =  input(" file name : ")
     key  = get_key()
     file_desc =  open(file,"r")
     text = file_desc.read()
     file_desc.close()
     if (clean == "yes"):
       text= clean_text(text)
       file_name = "Cleaner_"+file
       fd =  open(file_name ,"w")
       fd.write(text)
       fd.close()
       print(" \n The clean file is : ", file_name)
     text = chiffrer(text,key)
     name = "Crypt_"+file
     file=  open(name,"w")
     file.write(text)
     file.close()
     print ("  * successfully encrypted file : with key = ",key," \n  * The file result : ",name)
  elif (choice == "dec"): 
    print("\n---------------------------------- Decryption  ----------------------------------------\n")
    print (" #Indication : \n   Note that this is a probabilistic program based on frequency analysis \n   which means that the results are not necessarily 100% correct also \n   you may need to interact with the resulting keys explicitly \n   choosing the right key  \n" ) 
    print(" |+----------------------------+Important+------------------------------+|")
    print(" | Please make sure that the file which  contain text to be decrypted    |\n | is cleaned , mean no special characters  like  '! ? . 'é  ...         |")
    print (" |+-------------------------------------------------------------------- +|")
    print( "\n  * Enter the path of the file to be Decrypt * " )
    file = input("  File : ")
    file_des= open(file, "r")
    text = file_des.read()
    file_des.close()
    if (len(text)<1000): 
      print (" \n ERROR :   * Insufficient length  * \n ")
    else : 
      print("keyes : ")
      get_key_pro (crypt_analyse(text))
  else : 
    print(" Unknown  service!!")  

#le fiicher crypt_hlm est chiffre avec la key  : qG1o 
start()    




