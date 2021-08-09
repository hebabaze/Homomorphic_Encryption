from encryptFun import *
from tinydb import TinyDB, Query

import math
import random
import os
import dill
import socket
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
L={'0': 'Exit()', '1': 'Create Database','11':'Load existing DB', '2': 'Encrypt columns' ,'20':'encrypt Table','3': 'Send DataBase', '4': 'Calcul Sum', '5': 'Calcul Avg','6':'produit','7':'Restart'}
R=L.copy()
     
    #==> Fonction pour afficher la liste des Choix

def show(L):
    print('')
    for x,y in L.items():
      print(f"[{x}] {y}")
    print('\n')
    
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
    logging.info(f"Databases Created \n")
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
    for x in M:
        if x==0:
            return []
        else:
            C=[math.log(e) for e in M]
            Ce=[pub_key.encrypt(x) for x in C]
    return Ce
