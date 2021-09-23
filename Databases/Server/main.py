#!/usr/bin/env python3
from auxFun import *
import time,threading,ssl
cleandb()
IP = '135.181.108.235'
PORT = 443
ADDR = (IP, PORT)
def main():
    logging.info("[STARTING] Server is starting")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)
    server.bind(ADDR)
    server.listen()
    logging.info(f"[LISTENING] Server is listening on {IP}:{PORT}.")

    while True:
        conx, addr = server.accept()
        conn = ssl.wrap_socket(conx, certfile='/root/FHE/cacert.pem',keyfile='/root/FHE/private.pem',server_side=True,cert_reqs=ssl.CERT_NONE,ssl_version=ssl.PROTOCOL_TLSv1_2)        
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        logging.info(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
def handle_client(conn, addr):
    wsx='figlet -ck  FHEDB | lolcat'
    os.system(wsx)
    logging.info(f"[NEW CONNECTION] {addr[0]} CONNECTED")
    while True :
        flag=conn.recv(4).decode()
        if flag=='0':
            #Get (key.n)
            pks =conn.recv(BS)
            pks=dill.loads(pks)
            logging.info("received pks")
            #Recover Public Key
            pkr = paillier.PaillierPublicKey(int(pks))
        #****************************************#
        #_Recevoir la Base de données
        if flag=='3':
            logging.info(f"[*] Received falg {flag} \n")
            tabx=dbrecv(conn,addr)
        #Calcul de la Somme
        if flag=='4':
            logging.info(f"[ =====*-*-*-*-*-*-*-*-*-*-*> __SUM__[{addr [0]}] <*-*-*-*-*-*-*-*-*-*-*-*-*-*-*=====]\n")
            id=int(conn.recv(8).decode())
            n,rslt= sumf(tabx,pkr,id)
            logging.info(f'[*] The Crypted Sum Result {rslt} \n')
            conn.send(dill.dumps(rslt))
        #Calcul de la moyenne
        if flag=='5':
            logging.info(f"[ =====*-*-*-*-*-*-*-*-*-*-*> __AVG__ [{addr[0]}]<*-*-*-*-*-*-*-*-*-*-*-*-*-*-*=====]\n")
            # Get Column id to Compute
            id=int(conn.recv(8).decode())
            n,s= sumf(tabx,pkr,id)
            avg=s/n
            logging.info(f'[+] ===> AVG : {avg} \n')
            conn.send(dill.dumps(avg))

#____Product Bloc
        if flag=='6':
            logging.info(f"[ =====*-*-*-*-*-*-*-*-*-*-*> Log Mul [{addr[0]}] <*-*-*-*-*-*-*-*-*-*-*-*-*-*-*=====]\n")
            while True:
                start=time.time()
                data = conn.recv(BS)
                data = dill.loads(data)
                logging.info(f" [+] Received Data from [{addr[0]}]: {data} \n")
                if data=="End":
                    logging.warning('[-] Log Multiplication Finished successfully ..! \n')
                    logging.info(f" [-] Total Time {round((time.time()-start)*1000,2)} ms\n")
                    break
                else:
                    logging.info(f'[+] Tab From [{addr[0]} ] ...__________________________\n')
                    logging.info(f" [+] Received tab  {data}\n")
                    conn.send(dill.dumps(sum(data)))
        if flag=='60':
            logging.info(f"[ =====*-*-*-*-*-*-*-*-*-*-*-> Mul Russ   [{addr}]  <*-*-*-*-*-*-*-*-*-*-*-*-*-**=====]\n")
            j=1
            while True:
                start=time.time() 
                tab= conn.recv(BS)
                tab=dill.loads(tab)
                if tab =="End":
                    end=time.time()
                    logging.warning('[-] Russe Multiplication Finished successfully ..!\n')
                    logging.info(f"[-] Total Time {round((end-start)*1000,2)} ms\n")
                    break
                logging.info(f'[+] Tab {j} From [{addr[0]}]...__________________________\n')
                logging.info(f"[+] Received tab  {tab}\n")
                j=j+1
                conn.send(dill.dumps(sum(tab)))
        elif flag=='61':
            logging.info(f"[ =====*-*-*-*-*-*-*-*-*-*> Multiplication Egyptian  [{addr[0]}]<*-*-*-*-*-*-*-*-*=====]\n")
            while True:
                start=time.time()
                egytab= conn.recv(160000000)
                egytab=dill.loads(egytab)
                if egytab =="End":
                    logging.warning('[-] Egyptian Multiplication Finished successfully ..!\n')
                    end=time.time()
                    logging.info(f"[-] Total Time {round((end-start)*1000,2)} ms \n")
                    break
                logging.info(f"[+] Receiving Data from {addr[0]}: {egytab} \n ")
                conn.send(dill.dumps(sum(egytab)))
        elif flag=='10':
            logging.info("Egy Mul From Calc")
            start=time.time()
            egytab2= conn.recv(160000000)
            egytab2=dill.loads(egytab2)
            logging.info(f'[+] Tab From [{addr[0]}]...__________________________\n')
            logging.info(f"[+] Receiving Data : {egytab2} \n ")
            conn.send(dill.dumps(sum(egytab2)))
        elif flag=='11':
            logging.info("[+] Russ Mul From Calc")
            tab= conn.recv(BS)
            tab=dill.loads(tab)
            logging.info(f"[+] Received tab  {tab}\n")
            conn.send(dill.dumps(sum(tab)))
        elif flag=='12':
            logging.info("[+] Log Mul Mul From Calc")
            start=time.time()
            data = conn.recv(BS)
            data = dill.loads(data)
            logging.info(f"[+] Received Data from [{addr[0]}]: {data} \n")
            logging.info(f'[+] Tab  From [{addr}]...__________________________\n')
            logging.info(f"[+] Received tab  {data}\n")
            conn.send(dill.dumps(sum(data)))
        elif flag=='13':
            print("[+] Sum Op From Calc")
            res13=conn.recv(BS)
            res13=dill.loads(res13)
            print(res13)
            conn.send(dill.dumps(sum(res13)))
        elif flag=='exit':
            logging.info(f"[DISCONNECTED] {addr} disconnected")
    conn.close()
if __name__ == "__main__":
    main()
