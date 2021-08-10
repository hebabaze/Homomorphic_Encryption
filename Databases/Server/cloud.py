#!/usr/bin/env python3
from auxFun import *
import time
import jedi
import zlib
cleandb()
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
            flag=conn.recv(4).decode()
            #_Recevoir la Base de données
            if not flag:
                print("Not Flag")
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
            if flag=='5':
                # recevoir le id de colonne a calculé
                id=int(conn.recv(8).decode())
                n,s= sum(tabx,conn,pkr,id)
                avg=s/n
                print('[+] ===> AVG : ',avg)
                avg=dill.dumps(avg)
                print("n",n)
                conn.send(avg)
            ##Calcul de produit
            if flag=='6':
                print("[ =====> Log Mul <=====]")
                while True:
                    data = conn.recv(BS)
                    data = dill.loads(data)
                    if data=="End":
                        print(" Log Mul Out Data = End")
                        break
                    else:
                        sum=produit(data,conn)
                        xsum=dill.dumps(sum)
                        conn.send(xsum)
            if flag=='60':
                print("[ =====> Mul Russ <=====]")
                while True:
                    j=1
                    debut=time.time() 
                    tab= conn.recv(BS)
                    #tab=zlib.decompress(tab)
                    tab=dill.loads(tab)
                    if tab =="End":
                        end=time.time()
                        #.warning('Aucunes données reçus...Connection terminée..!')
                        #logging.info(f"Total Time {round((end-debut)*1000,2)} ms")
                        print('Aucunes données reçus...Mul_Russ terminée..!')
                        print(f"Total Time {round((end-debut)*1000,2)} ms")
                        break
                    print(f'tab {j} Recus')
                    j=j+1
                    sum=0
                    for x in tab :
                        sum += x
                    sum=dill.dumps(sum)
                    #sum=zlib.compress(sum)
                    conn.send(sum)
            if flag=='0':
                break
    

