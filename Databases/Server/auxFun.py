import os.path,zlib
from os import path
from pathlib import Path
from tqdm import tqdm# la barre de transfer
import os,time
import math
import random
from tinydb import TinyDB, Query
import dill # sÃ©rialisation
import socket
BS = 8132

# Standard loopback interface address (localhost)
        # Port to listen on (non-privileged ports are > 1023)
###########################################
def cleandb():
    import os
    try:
        cmd = 'rm /tmp/*.db'
        os.system(cmd)
    except:
        print('Clean directory')
def affiche(tabx): # Affichage de tableu
    print('')
    for Y in tabx:
        for x,y in Y.items():
            print(f"{x} : {y}",end = '|')
        print('')
###################################
from phe import paillier
def sumf(tabx,conn,pkr,id): # fonction de calcul de somme selon l'id de colonne
    sum=0
    n=0
    for x in tabx :
        n+=1
        sum+=paillier.EncryptedNumber(pkr, int(list(x.values())[id][0]), int(list(x.values())[id][1]) )
    print(f'la somme calculÃ© {sum}')
    return n,sum
####################################################
def produit(data,conn): #Function used in Log mul 
    print("The Data :",data)
    if not data or data =="End":
        print(" No Data Detected !")
        return 1
    else:
        sum=0
        for x in data :
            sum+=x
            print(f'le produit calculÃ© {sum}')
    print("Final :_________",sum)
    return sum
############################################################
def dbrecv(conn):
    dbname=conn.recv(16).decode()
    dbname = os.path.basename(dbname)
    print(f"[+] the received file name : {dbname}")
    print(f"Waitting for {dbname}..>>",end='..')
    while True:
        dirs = os.listdir( "/tmp/" )
        if dbname in dirs:
            print("Got it !")
            break
        else:
            time.sleep(1)
            print("...",end='...')    
    print("Done receiveing")
    os.chdir("/tmp")
    print('The crypted file stocked in:      ', os.getcwd())
    received_db= TinyDB(dbname)  # load database
    print("\n")
    print('The crypted file stocked in:      ', os.getcwd())
    print('Listes des tableaux ',received_db.tables())
    try:
        x=received_db.tables()
    except:
        print("Reciveing data failed")
        conn.send("Reciveing data failed".encode())
        return  
    try:
        tabx=received_db.table(list(x)[0])
        conn.send("Receiving Database Successfully".encode())
        print("Receiving Database Successfully")
    except:
        conn.send("Reciveing data failed".encode())
        return          
    print("Received Table Head values :")
    for i in range(1,3):
        rdic=tabx.get(doc_id=i) # to check value type
        print(rdic)
    print("*************************************************************************")
    print(tabx.all())
    return tabx
######################################################

