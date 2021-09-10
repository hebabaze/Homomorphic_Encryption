#!/usr/bin/env python3
from auxFun import *
import time,ssl
IP = '135.181.108.235'
PORT = 65432
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#-=-=-Création de Socket
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)
s.bind((IP, PORT))
print("Listening for connection...")
s.listen(10)
#from into while
conx, addr = s.accept()
print(f'Etablished connection ..[{addr[0]}] connected! \n')
conn = ssl.wrap_socket(conx, certfile='cacert.pem',keyfile='private.pem',server_side=True,cert_reqs=ssl.CERT_NONE,ssl_version=ssl.PROTOCOL_TLSv1_2)
while True : 
    flag=conn.recv(4).decode()
    if flag=='0':
    #Get Public Key
    #recuperer la clé clé public de paiiler
        print("From Flag  conn =",conn)
        print("Received falg",flag)
        cleandb()
        pks =conn.recv(BS)
        pks=dill.loads(pks)
        print("received pks",pks)
        conn.send("Thanks".encode())
        #reconstruir la clé  public de paiiler
        pkr = paillier.PaillierPublicKey(int(pks))
    elif flag=='3':
        print("From Flag 3 conn =",conn)
        print("Received falg",flag)
        tabx=dbrecv(conn)
    #Calcul de la Somme
    elif flag=='4':
        # recevoir le id de colonne a calculé
        id=int(conn.recv(8).decode())
        n,xsum= sumf(tabx,conn,pkr,id)
        xsum=dill.dumps(xsum)
        conn.send(xsum)
    #Calcul de la moyenne
    elif flag=='5':
        # recevoir le id de colonne a calculé
        id=int(conn.recv(8).decode())
        n,s= sumf(tabx,conn,pkr,id)
        avg=s/n
        print('[+] ===> AVG : ',avg)
        avg=dill.dumps(avg)
        print("n",n)
        conn.send(avg)
    ##Calcul de produit
    elif flag=='6':
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
    elif flag=='60':
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
    elif flag=='exit':
        break


