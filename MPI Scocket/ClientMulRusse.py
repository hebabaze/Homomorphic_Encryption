import socket #communication entre serveur et client
import pickle
from phe import paillier
import math
import time
import zlib
import logging
header=9032 #en octet
HOST = '192.168.1.10'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
#__Configuration de logging
format="%(asctime)s.%(msecs)03d--%(levelname)s : %(message)s"
logging.basicConfig(format=format,level=logging.INFO,datefmt="%H:%M:%S")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True  :
        Keys={ 0:'exit()',10:64 ,1:128,2:256,3:512,4:1024,5:1536,6:2048 ,7:4096}
        logging.info(f'KeysId : \nXXXXXXXXXXXXXXXXXX : [{Keys}]')
        try :
            x=eval(input(f"Saisir l'id de clé or X for Exit >> "))
            if x== 0:
                print(f'\nGood Bye..!')
                break
            pub_key,priv_key=paillier.generate_paillier_keypair(n_length=Keys[x])

        except :
            print("Inserer une Valeur entre 1 et 6")
      
        #__Saisie des Valeurs
        m1 = eval(input(f"Saisir la valeur de m1 >> "))
        m2 = eval(input(f"Saisir la valeur de m2 >> "))
    #BLOC I : __Encrypt Data_______________________________________
        start=time.time()
        tab=[]
        while m1>0:
            if m1%2==1 :
                e2=pub_key.encrypt(m2)
                tab.append(e2)    
            m1=m1//2
            m2=m2*2
        tab=pickle.dumps(tab)
        tab=zlib.compress(tab)
        s.send(tab)
        #############___Receiv Sum
        result=s.recv(header)
        result=zlib.decompress(result)
        result=pickle.loads(result)
        ##################_____Decrypt
        result=priv_key.decrypt(result)
        end=time.time()
        print('le temps écoulé ',round((end-start)*1000,2))
        print(f"le resultat est : {result}")