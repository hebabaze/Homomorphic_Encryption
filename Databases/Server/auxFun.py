from tqdm import tqdm# la barre de transfer
import os
import math
import random
from tinydb import TinyDB, Query
import dill # sérialisation
import socket
BS = 8132
HOST = '192.168.1.10'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
import logging # journalisation 
#__Configuration de logging
format="%(asctime)s.%(msecs)03d--%(levelname)s : %(message)s"
logging.basicConfig(format=format,level=logging.INFO,datefmt="%H:%M:%S")
###########################################
def cleandb():
    import os
    try:
        cmd = 'rm *.db'
        os.system(cmd)
    except:
        logging.info('Clean directory')
##########################
def affiche(tabx): # Affichage de tableu
    print('')
    for Y in tabx:
        for x,y in Y.items():
            print(f"{x} : {y}",end = '|')
        print('')
###################################
from phe import paillier
def sum(tabx,conn,pkr,id): # fonction de calcul de somme selon l'id de colonne
    sum=0
    n=0
    for x in tabx :
        n+=1
        sum+=paillier.EncryptedNumber(pkr, int(list(x.values())[id]), 0) 
    print(f'la somme calculé {sum}')
    return n,sum
####################################################
def produit(data,conn): # 
    sum=0
    for x in data :
        sum+=x
    print(f'le produit calculé {sum}')
    xsum=dill.dumps(sum)
    conn.send(xsum)
    
############################################################
def dbrecv(conn,BS):
    SEPARATOR='~'
    received =conn.recv(BS).decode('utf-8')     # recevoir le nom de fichier et son taille 
    fname, filesize = received.split(SEPARATOR)
    # remove absolute path if there is
    fname = os.path.basename(fname) 
    # convert filesize to integer 
    filesize = int(filesize)
    fname=fname+'.db'
    #####################################
    with open(fname, "wb") as f:
        while True :
            for i in tqdm(range(64,filesize,64),unit="Bytes",unit_divisor=64,desc=f"Sending [{fname}]",colour= 'green'):
                bytes_read = conn.recv(64)
                f.write(bytes(bytes_read))
                if filesize-i < 64 :
                    bytes_read = conn.recv(filesize-i)
                    f.write(bytes(bytes_read))
            break
    ################################################
    db= TinyDB(fname)  # load database
    print("\n")
    print('Listes des tableaux ',db.tables())
    x=db.tables()
    tabx=db.table(list(x)[0])
    print("le tableau reçus :")
    affiche(tabx)
    return tabx
######################################################
