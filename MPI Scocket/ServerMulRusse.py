import socket
import pickle
from phe import paillier
import math
import time
import zlib
import logging
import jedi
HOST = '192.168.1.10'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
header=9032
#__Configuration de logging
format="%(asctime)s.%(msecs)03d--%(levelname)s : %(message)s"
logging.basicConfig(format=format,level=logging.INFO,datefmt="%H:%M:%S")
#=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-==-
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    #-=-=-Création de Socket
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    s.bind((HOST, PORT))
    s.listen(3)
    conn, addr = s.accept()
    logging.info(f"[STARTING] Server ..!")
    with conn:
        logging.info(f'Connexion Etablie ..[{addr[0]}] est connecté! \n')
        while True:
            debut=time.time() 
            tab= conn.recv(header)
            if not tab :
                end=time.time()
                logging.warning('Aucunes données reçus...Connection terminée..!')
                logging.info(f"Total Time {round((end-debut)*1000,2)} ms")
                break
            logging.info('Tous les paquets sont reçus')
            sum=0
            tab=zlib.decompress(tab)
            tab=pickle.loads(tab)
            for x in tab :
                sum += x
            sum=pickle.dumps(sum)
            sum=zlib.compress(sum)
            conn.send(sum)
            logging.info('les deux Fonctions sont exécutées \n')
s.close() 