#!/usr/bin/env python3
from auxFun import *
import time
cleandb()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #-=-=-Création de Socket
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)
    s.bind((HOST, PORT))
    print("Listening for connection...")
    s.listen(10)
    conn, addr = s.accept()
    print(f'Etablished connection ..[{addr[0]}] connected! \n')
    with conn:

        while True :
            flag=conn.recv(4).decode()
            if flag=='0':
                #Get Public Key
                #recuperer la clé clé public de paiiler
                pks =conn.recv(BS)
                pks=dill.loads(pks)
                print("received pks")
                #reconstruir la clé  public de paiiler
                pkr = paillier.PaillierPublicKey(int(pks))
            #****************************************#
            
            #_Recevoir la Base de données
            #if not flag:
            #    print("Not Flag")
            if flag=='3':
                print("Received falg",flag)
                tabx=dbrecv(conn)
            #Calcul de la Somme
            if flag=='4':
                # recevoir le id de colonne a calculé
                id=int(conn.recv(8).decode())
                n,xsum= sumf(tabx,conn,pkr,id)
                xsum=dill.dumps(xsum)
                conn.send(xsum)
            #Calcul de la moyenne
            if flag=='5':
                # recevoir le id de colonne a calculé
                id=int(conn.recv(8).decode())
                n,s= sumf(tabx,conn,pkr,id)
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
                    tab=dill.loads(tab)
                    if tab =="End":
                        end=time.time()
                        #.warning('Aucunes données reçus...Connection terminée..!')
                        #logging.info(f"Total Time {round((end-debut)*1000,2)} ms")
                        print('Aucunes données reçus...Mul_Russ terminée..!')
                        print(f"Total Time {round((end-debut)*1000,2)} ms")
                        break
                    print(f'tab {j} Recus')
                    print("Received tab ",tab)
                    j=j+1
                    sum=0
                    for x in tab :
                        sum += x
                    sum=dill.dumps(sum)
                    conn.send(sum)
            if flag=='exit':
                break

