from encryptFun import *
from tinydb import TinyDB, Query

import math
import random
import os
import dill
import socket
import zlib
HOST = '192.168.1.10'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
SEPARATOR = "<SEPARATOR>"
BS = 4096 # send 4096 bytes each time step
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
#__Configuration de logging
import logging
format="%(asctime)s.%(msecs)03d--%(levelname)s : %(message)s"
logging.basicConfig(format=format,level=logging.INFO,datefmt="%H:%M:%S")

# [+] : BLOC D'ENVOI
def sendid(x,pkr):
    s.send(x.encode())
    id=input('Saisir l\'id de colonne à calculer >__ ')
    s.send(id.encode()) # id de colonne concerné

# [+] : BLOC D'AFFICHAGE _____________________________________________________________________________________________________

    #==> dictonnaire des choix
L={'0': 'Exit()', '1': 'Create Database','11':'Load existing DB', '2': 'Encrypt columns' ,'20':'encrypt Table','3': 'Send DataBase', '4': 'Calcul Sum', '5': 'Calcul Avg','6':'produit Log Mul','60':'Produit Russ Mul','7':'Restart'}
R=L.copy()
     
    #==> Fonction pour afficher la liste des Choix

def show(L):
  
    for x,y in L.items():
      print(f"[{x}] {y}")

    
    #==> Fonction pour Afficher le contenu de tableur tinydb
    
def affiche(tabx):
    print('')
    for Y in tabx:
        for x,y in Y.items():
            print(f"{x} : {y}",end = '|')
        print('')
        

#_[+] : BLOC DE CREATION DE LA BASE DE DONNÉES____________________________________________________________________________
        
        #Fonction pour créer la base de donnée et le tableau
def loaddb():
    cmd = 'python C:\\Users\\Root\\Documents\\GitHub\\Homomorphic_Encryption\\Databases\\WindowsClient\\creatDB.py'
    os.system(cmd)
    basepath ='C:\\Users\\Root\\Documents\\GitHub\\Homomorphic_Encryption\\Databases\\WindowsClient'
    List_db=[]
    for entry in os.listdir(basepath):
        if entry.endswith('.db'):
            List_db.append(entry)
    logging.info(f"List des DBs {List_db}\n")
    indice=int(input("[*] Saisir L'id da base de données >>.. "))
    fname=List_db[indice]
    db = TinyDB(fname)
    tabx=db.table('Hr')
    affiche(tabx)
    rdic=tabx.get(doc_id=1) # to check value type
    columns=list(rdic.keys())
    return columns,tabx,fname,db

def creatdb():
  x=input('[*][Database name ] : >__ ')
  fname=x+'.db'
  dbase=TinyDB(fname)
  mytable=input('[*][Table name] : >__  ')
  crypttable=rsacrypt(mytable)
  tab=dbase.table(crypttable)
  return fname,tab

        # Fonction pour définir les noms des colonnes # Taper 0 pour quitter ()

def insrow() :
  columns=[]  # list qui contiendra les nom des colonnes 
  i=0
  while True :
    x=input(f'[*] [column [{i}] name] : >__ ')
    cryptcoulmn=rsacrypt(x)
    if x=='0':
      break
    columns.append(cryptcoulmn)
    i+=1
  return columns
        # Fonction pour inserer les valeurs de chaque Colonne # Taper 0 pour quitter ()

def insVal(columns,tab,privkey):
  i=0
  while True:
    temp=[]
    dicto={}
    for x in columns :
      z=input(f"[*] [record [{i}] insert [{rsadecrypt(x, privkey)}] ] : >__ ")
      if z=='0':
        break    
      temp.append(z)
    if z=='0':
      break
    i+=1
    for j in range(len(columns)):
      dicto[columns[j]]=temp[j]
    tab.insert(dicto)# pour savoir le type des valeurs saisies
    
#__[+] : BLOC PRODUIT _______________________________________________________________________________________________________

def rsadecrypt(x,privkey):
    x=unhexlify(x)
    dec=rsa.decrypt(x,privkey)
    return dec.decode()
def applylog(tabx,id,pkr):
    L=[]
    pkr = paillier.PaillierPublicKey(int(pkr))
    for x in range(1,len(tabx)+1):
        Far=tabx.get(doc_id=x)
        L.append(list(Far.values())[id])
    P=[paillier.EncryptedNumber(pkr, x, 0) for x in L]
    M=[priv_key.decrypt(x) for x in P]
    for x in M: # Check 0 result
        if x==0:
            return []
        else:
            C=[math.log(e) for e in M]
            Ce=[pub_key.encrypt(x) for x in C]
    return Ce
def RussMul(s,pub_key,pkr,BS,tabx,id):
  L=[] # Pour Stocker Les Valeurs à calculer 
  pkr = paillier.PaillierPublicKey(int(pkr)) #pkr=pub_key.n pour reconstruire le ciphertext
  # Stocker les valeur à calculer 
  for x in range(1,len(tabx)+1):
        Far=tabx.get(doc_id=x)
        L.append(list(Far.values())[id])
  P=[paillier.EncryptedNumber(pkr, x, 0) for x in L]
  #Decrypter les valeur à traiter
  M=[priv_key.decrypt(x) for x in P]
  for x in M: # Check 0 result
    if x==0:
      logging.critical("0 Result Dectected")
      return "Zéro Result Detected!.."
    else:
      i=0
      j=1
      m1=M[i]
      for i in range(0,len(M)-1):
        tab=[]
        m2=M[i+1]
        while m1>0:
          if m1%2==1 :
            e2=pub_key.encrypt(m2)
            tab.append(e2)
          m1=m1//2
          m2=m2*2
        ##########___Send tab
        logging.info(f"Sending Table n° {j} ==> {tab}")
        j+=1
        tab=dill.dumps(tab)
        tab=zlib.compress(tab)
        s.send(tab)
        #############___Receiv Sum
        result=s.recv(BS)
        result=zlib.decompress(result)
        result=dill.loads(result)
        ##################_____Decrypt
        result=priv_key.decrypt(result)
        logging.info(f"Multiplication n° {j} Result :[{result}]")
        m1=result
        #################__BreakOut
    logging.info(f"Final Result :[{result}]")
    tab=[]
    tab=dill.dumps(tab)
    tab=zlib.compress(tab)
    s.send(tab)
    return "Completed Task"  
