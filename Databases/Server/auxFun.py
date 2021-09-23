import os.path,zlib
from os import path
from pathlib import Path
import os,time, math,dill,socket,logging
from tinydb import TinyDB, Query
BS = 8132
# Port to listen on (non-privileged ports are > 1023)
###########################################
format="%(asctime)s.%(msecs)03d--%(levelname)s : %(message)s"
logging.basicConfig(format=format,level=logging.INFO,datefmt="%H:%M:%S")
#logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
###########################################
def cleandb():
    import os
    try:
        cmd = 'rm /tmp/*.db'
        os.system(cmd)
    except:
        logging.info('Clean directory')
def affiche(tabx): # Affichage de tableu
    logging.info('')
    for Y in tabx:
        for x,y in Y.items():
            print(f"{x} : {y}",end = '|')
        logging.info('')
###################################
from phe import paillier
def sumf(tabx,pkr,id): # fonction de calcul de somme selon l'id de colonne
    resulta=0
    n=0
    for x in tabx :
        n+=1
        resulta+=paillier.EncryptedNumber(pkr, int(list(x.values())[id][0]), int(list(x.values())[id][1]) )
    return n,resulta

############################################################
def dbrecv(conn,addr):
    dbname=conn.recv(128).decode()
    dbname = os.path.basename(dbname)
    logging.info(f"[+] The received file name : {dbname}")
    print(f"[*] Waitting for {dbname} from [ {addr[0]} ]..>>",end='..')
    while True:
        dirs = os.listdir( "/tmp/" )
        if dbname in dirs:
            #logging.info("Got it !")
            break
        else:
            time.sleep(1)
            print("...",end='...')    
    logging.info(f"[+] Done receiveing {dbname} from [ {addr[0]} ] ")
    os.chdir("/tmp")
    logging.info(f"[-*-] The crypted file stocked in: {os.getcwd()}")
    received_db= TinyDB(dbname)  # load database
    logging.info("\n")
    logging.info(f'[-*-] Tables Lists : {received_db.tables()}')
    try:
        x=received_db.tables()
    except:
        logging.info("[-] Reciveing data failed")
        conn.send("[-] Reciveing data failed".encode())
        return  
    try:
        tabx=received_db.table(list(x)[0])
        conn.send("[+] Receiving Database Successfully from [ {addr[0]} ]".encode())
    except:
        conn.send("[-] Reciveing data failed".encode())
        return          
    logging.info(f"[*] Head values of Received Table from [ {addr[0]} ].. ")
    for i in range(1,3):
        rdic=tabx.get(doc_id=i) # to check value type
        logging.info(rdic)
        print('\n')
    logging.info("*****************-*-*-*-*-*-**********************************************************")
    logging.info("______________________________________________________________________________________\n")
    return tabx

