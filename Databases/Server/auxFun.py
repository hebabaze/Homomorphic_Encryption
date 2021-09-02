from pathlib import Path
from tqdm import tqdm# la barre de transfer
import os
import math
import random
from tinydb import TinyDB, Query
import dill # sérialisation
import socket
BS = 8132
HOST = '192.168.1.107'
# Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
###########################################
def cleandb():
    import subprocess
    try:
        cmd0 = 'del *x.db';os.system(cmd0)
        cmd = 'del C:\\Users\\Root\\Documents\\GitHub\\Homomorphic_Encryption\\Databases\\Server\\*.db';os.system(cmd)
        cmd1 = 'del C:\\Users\\Root\\Desktop\\KivY\\KivyFheDb\\*x.db';os.system(cmd)
        cmd2 = 'del C:\\Users\\Root\\Documents\\GitHub\\Homomorphic_Encryption\\Databases\\Server\\*.db';os.system(cmd)
        cmd3 ='del rC:/Users/Root/Documents/GitHub/Homomorphic_Encryption/Databases/Server/*.db';os.system(cmd)
        subprocess.Peopen(cmd0,shell=True)
        subprocess.Peopen(cmd,shell=True)
        subprocess.Peopen(cmd1,shell=True)
        subprocess.Peopen(cmd2,shell=True)
        subprocess.Peopen(cmd3,shell=True)
    except:
        print('Clean directory')
##########################
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
        sum+=paillier.EncryptedNumber(pkr, int(list(x.values())[id]), 0) 
    print(f'la somme calculé {sum}')
    return n,sum
####################################################
def produit(data,conn):
    print("The Data :",data)
    if not data or data =="End":
        print(" Not Data Detected !")
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
    fname =conn.recv(BS).decode('utf-8')     # recevoir le nom de fichier et son taille
    filesize =conn.recv(8).decode('utf-8')
    # remove absolute path if there is
    fname = os.path.basename(fname)
    print("this is fname",fname)
    # convert filesize to integer
    filesize = int(filesize)
    print("this is filesize",filesize)
    fname=fname+'.db'
    #####################################
    print("Start Receiving File")
    with open(fname, "wb") as f:
        bytes_read = conn.recv(filesize)
        f.write(bytes(bytes_read))
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
