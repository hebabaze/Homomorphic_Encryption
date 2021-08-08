from phe import paillier 
import libnum
import math
from mpi4py import MPI
import time
comm=MPI.COMM_WORLD
rank = comm.rank
size = comm.size
name = MPI.Get_processor_name()
pub_key,priv_key=paillier.generate_paillier_keypair(n_length=128)
###
def crypt_send(m1,m2,pub_key,tag1,tag2):
    e1=pub_key.encrypt(m1)
    e2=pub_key.encrypt(m2)
    comm.send(e1,dest=1,tag=tag1)
    comm.send(e2,dest=1,tag=tag2)
###
def decrypt(priv_key,e):
        m=priv_key.decrypt(e)
        return m
###
def CloudProvider(tagx,tagy):
    if rank==1:
        e1=comm.recv(source=0,tag=tagx)
        e2=comm.recv(source=0,tag=tagy)
        e=e1+e2
        comm.send(e,dest=0,tag=tagx+tagy)
##########################   Multiplcation Russe Protocol  #####################################
def clientMulRusse(m1,m2,pub_key,priv_key):
    start=time.time()
    #e2=pub_key.encrypt(m2)
    tabs=[]
    if rank==0:
        while m1>0:
            if m1%2==1 :
                e2=pub_key.encrypt(m2)
                tabs.append(e2)    
            m1=m1//2
            m2=m2*2           
        comm.send(tabs,dest=1,tag=33)
        sumr=comm.recv(source=1,tag=66)
        m=priv_key.decrypt(sumr)
        print(" \n \033[1;34;48m ######  Fonction Russe Mul______\n\033[0m")
        #print("\033[1;31;48m [ {} : ] \033[0m ==> Crypte {} avec Mul_Russe ".format(name,m2))
        print("\033[1;32;48m [ {} : ] \033[0m==> Decrypte avec Mul_Russe [le m = {} ]  \n".format(name,m))
        print(f"\n===> le temps de multiplication Russe est : {(time.time() - start)*1000} ms")
    else:
        sum=0
        tabr=comm.recv(source=0,tag=33)
        for x in tabr :
            sum=sum+x
        comm.send(sum,dest=0,tag=66)

################################################Log Mul Protocol ################################
def logMul(m1,m2):
    start=time.time()
    if rank==0:
        l1=math.log(m1)
        l2=math.log(m2)
        debutCrypt=time.time()
        crypt_send(l1,l2,pub_key,4,5)
        #print(f"===> le temps pour  crypter et envoyer les deux messages  : {(time.time() - debutCrypt)*1000} ms")
        e=comm.recv(source=1,tag=9)
        debutDecrypt=time.time()
        m=decrypt(priv_key,e)
        #print(f"\n ===> le temps pour  décrypter le messages est : {(time.time() - debutDecrypt)*1000} ms")
        message=math.exp(m)
        print("\n \033[1;34;48m ######  Fonction Log Mul ___________: \n\033[0m ")
        print("\033[1;32;48m [ {} : ] \033[0m ==> resultat de decryptage avec la methode Log_Mul est : {} " .format(name,message))
        print(f"\n===> le temps pour appliquer le protocole de logarithme est : {(time.time() - start)*1000} ms")
    else :
        #
        #print("\033[1;31;48m [ {} : ] \033[0m  ==> Crypte avec la méthode Log_Mul  {} et {} ".format(name,m1,m2))
        CloudProvider(4,5)
        
    #================================== Main () :===========================#
m1=7
m2=9
if rank==0:
    print(" \n \033[1;34;48m######  Les paramétres initails______\n\033[0m")
    print("\033[1;32;48m [ {} : ] \033[0m ==> prends les paramétres suivant comme entrées {} et {}  ".format(name,m1,m2))
    crypt_send(m1,m2,pub_key,tag1=1,tag2=2)
    s=comm.recv(source=1,tag=3)
    sum=decrypt(priv_key,s)
    print(" \n \033[1;34;48m######  Affichage de La Somme : ______\n\033[0m")
    print("\033[1;32;48m [ {} : ] \033[0m ==> le resultat de Somme est  {} ".format(name,sum))   
if rank==1:
    CloudProvider(1,2)

logMul(m1,m2)  
clientMulRusse(m1,m2,pub_key,priv_key)
