#!/usr/bin/env python3
from auxFun import *
from encryptFun import * 

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
            logging.info(" Database sent..!! \n")
            show(L)

#######Receiv Sum
        elif x=='4':
            sendid(x,pkr)
            sum=s.recv(BS)
            sum=dill.loads(sum)
            sum=priv_key.decrypt(sum)
            logging.info(f" [+] Resultat de la somme est [{sum}]")
            show(L)
#######Receiv AVG
        elif x=='5':
            sendid(x,pkr)
            avg=s.recv(BS)
            avg=dill.loads(avg)
            avg=priv_key.decrypt(avg)
            logging.info(f" [+] Resultat d'AVG {avg}")
            show(L)

#######Calculer le Produit d'une Colonne 
        elif x=='6':
            id=int(input('Saisir l\'id de colonne à calculer >__ '))
            Lprod=applylog(tabx,id,pkr)
            if not Lprod:
                logging.warning(" Product equal to zéro")
            else:
                s.send(x.encode())
                logging.info("\n {Lprod} \n")
                Lprod=dill.dumps(Lprod)
                s.send(Lprod)
                
                prod=s.recv(4096)
                prod=dill.loads(prod)
                prod=priv_key.decrypt(prod)
                logging.warning(f"Prod received before exp {prod}")
                try:
                    #709.78271 is the largest value I can compute the exp of on my machine
                    prod=round(math.exp(prod))
                except OverflowError:
                    logging.warning("Input value is greater than allowed limit")
                logging.info(f" [+] Resultat produit  est [{prod}]")
                show(L)
###___Réinitiliser la liste des choix
        elif x=='7':
            L=R.copy()
            show(L)
###____quiter()
        elif x=='0':
            cmd = 'rm *.db'
            os.system(cmd)
            break
        elif x not in list(L.keys()):
             logging.error("Insert a correct Choice !")

