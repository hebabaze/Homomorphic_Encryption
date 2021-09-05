from pathlib import Path
from tqdm import tqdm# la barre de transfer
import os
import math
import random
from tinydb import TinyDB, Query
import dill # sérialisation
import socket
BS = 8132
HOST = '135.181.108.235'
# Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
###########################################
def cleandb():
    import os
    try:
        cmd = 'rm *.db'
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
    print(f'la somme calculé {sum}')
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
            print(f'le produit calculé {sum}')
    print("Final :_________",sum)
    return sum
############################################################
def dbrecv(conn,BS):
    SEPARATOR='@'
    fname =conn.recv(128).decode('utf-8')     # recevoir le nom de fichier et son taille 
    filesize = conn.recv(4).decode('utf-8')
    # remove absolute path if there is
    fname = os.path.basename(fname) 
    print("This is file name",fname)
    print("This is File Size",filesize)
    # convert filesize to integer 
    filesize = int(filesize)
    print("This is File Size",filesize)
    fname=fname+'.db'
    #####################################
    print("Start receiving file data")
    with open(fname, "wb") as f:
        while True :
            for i in tqdm(range(64,filesize,64),unit="Bytes",unit_divisor=64,desc=f"Receiving [{fname}]",colour= 'green'):
                bytes_read = conn.recv(64)
                f.write(bytes(bytes_read))
                if filesize-i < 64 :
                    bytes_read = conn.recv(filesize-i)
                    f.write(bytes(bytes_read))
            break
    ################################################
    db= TinyDB(fname)  # load database
    print("\n")
    print('The crypted file stocked in:      ', os.getcwd())
    print('Listes des tableaux ',db.tables())
    x=db.tables()
    tabx=db.table(list(x)[0])
    print("le tableau reçus :")
    affiche(tabx)
    return tabx
######################################################

