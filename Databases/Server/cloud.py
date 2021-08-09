#!/usr/bin/env python3
from aux import *


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #-=-=-Création de Socket
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind((HOST, PORT))
    s.listen(3)
    conn, addr = s.accept()
    with conn:
        print(f'Connexion Etablie ..[{addr[0]}] est connecté! \n')
         #Get Public Key
        #recuperer la clé clé public de paiiler
        pks =conn.recv(BS)
        pks=dill.loads(pks)
        #reconstruir la clé  public de paiiler
        pkr = paillier.PaillierPublicKey(int(pks))
        while True :
            flag=conn.recv(8).decode()
            #_Recevoir la Base de données 
            if flag=='3':
                tabx=dbrecv(conn,BS)
            #Calcul de la Somme     
            if flag=='4':
                # recevoir le id de colonne a calculé
                id=int(conn.recv(8).decode())
                n,xsum= sum(tabx,conn,pkr,id)
                xsum=dill.dumps(xsum)
                conn.send(xsum)
            #Calcul de la moyenne
            elif flag=='5':
                # recevoir le id de colonne a calculé
                id=int(conn.recv(8).decode())
                n,s= sum(tabx,conn,pkr,id)
                avg=s/n
                print('[+] ===> AVG : ',avg)
                avg=dill.dumps(avg)
                print("n",n)
                conn.send(avg)
            ##Calcul de produit
            elif flag=='6':
                data = conn.recv(16000)
                data = dill.loads(data)
                produit(data,conn)
        
            elif flag=='0':
                break
    

