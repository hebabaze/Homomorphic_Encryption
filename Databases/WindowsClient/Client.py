#!/usr/bin/env python3
from auxFun import *
from encryptFun import * 
#with declared Client Socket
with s:
    s.connect((HOST, PORT))
    logging.info(f"[+] Connecting to {HOST}:{PORT}")
    logging.info("[+] Connected.")
    pks=dill.dumps(pkr)
    s.send(pks) # L'envoie de clé public
    show(L)
    while True:
        x=input(">> ..")
#----11---Load Existing Database :
        if x== '11':
            columns,tabx,fname,db=loaddb()
            show(L)
# ---1---Create Database
        if x=='1' : 
            del L[x]
            fname,tabx=creatdb()
            columns=insrow()
            insVal(columns,tabx,privkey)
            affiche(tabx)
            show(L)
# ---2---Encrypt DataBase
        elif x=='2':
            encrypt(tabx,columns)
            affiche(tabx)
            show(L)
        elif x=='20':
            tabx=crypt_table(tabx,db)
            logging.info(" Table Crypted Succefuly")
# ---3---Send DataBase
        elif x=='3':
            s.send(x.encode())
            dbsend(fname,BS,s)
            logging.info(" Database sent..!!")
            show(L)

#######Receiv Sum
        elif x=='4':
            sendid(x)
            sum=s.recv(BS)
            sum=dill.loads(sum)
            sum=priv_key.decrypt(sum)
            logging.info(f" [+] Resultat de la somme est [{sum}]")
            show(L)
#######Receiv AVG
        elif x=='5':
            sendid(x)
            avg=s.recv(BS)
            avg=dill.loads(avg)
            avg=priv_key.decrypt(avg)
            logging.info(f" [+] Resultat d'AVG {avg}")
            show(L)

#######Calculer le Produit d'une Colonne 
        elif x=='6':
            s.send(x.encode())
            id=input('Saisir l\'id de colonne à calculer >__ ')
            applylog(tabx,int(id),pkr)
            show(L)
        elif x=='60':
            s.send(x.encode())
            id=input('Saisir l\'id de colonne à calculer >__ ')
            RussMul(s,pub_key,pkr,BS,tabx,int(id))
###___Réinitiliser la liste des choix
        elif x=='7':
            L=R.copy()
            show(L)
###____quiter()
        elif x=='0':
            cmd = 'del *.db'
            os.system(cmd)
            break
        elif x not in list(L.keys()):
             logging.error("Insert a correct Choice !")

