from auxFun import *
import rsa
(pubkey, privkey) = rsa.newkeys(512)
from binascii import hexlify , unhexlify
from phe import paillier
pub_key,priv_key=paillier.generate_paillier_keypair(n_length=128)
pkr=pub_key.n
import os
from tqdm import tqdm
# __ [+] : BLOC DE CRYPTAGE __________________________________________________________________________________________________

def rsacrypt(data):       # Fonction de Cryptage RSA
  message=data.encode()
  crypto = rsa.encrypt(message, pubkey)
  crypto = hexlify(crypto).decode()
  return crypto

def enciph(y):            # get encipher text
  x=pub_key.encrypt(y)
  return x.ciphertext()

def paillierEncr(x):      #Crypter les colonnes de types int
  def transform(doc):
    doc[x]=enciph(int(doc[x]))
  return transform

def rsaEncr(x):    #Crypter les colonnes de types String
  def transform(doc):
    doc[x]=rsacrypt(doc[x])
  return transform
def encrypt(tabx,columns):   # crypter une colonne
    e=int(input('[*] [row id to encrypt ?] : >__ '))
    rdic=tabx.get(doc_id=1) # to check value type
    if str(rdic[columns[e]]).isalpha():
        tabx.update(rsaEncr(columns[e]))
    elif not str(rdic[columns[e]]).isalpha() :
        tabx.update(paillierEncr(columns[e]))
def crypt_table(tabx,db):
    #tabname=rsacrypt(tabx.name)
    tabrx = db.table('Xm')
    for x in tabx :
        d={}
        for a,b in x.items() :
            if str(b).isalpha():
                d[rsacrypt(a)]=rsacrypt(b)
            elif not str(b).isalpha() :
                d[rsacrypt(a)]=enciph(int(b))
        tabrx.insert(d)
    db.drop_table(tabx.name)
    return tabrx

##__ Fonction pour envoyer la base de donnée

def dbsend(fname,BS,s):
    SEPARATOR = "~"
    filesize = os.path.getsize(fname)
    s.send(f"{rsacrypt(fname)}{SEPARATOR}{filesize}".encode('utf-8'))
    with open(fname, "rb") as f:
        while True :
            for i in tqdm(range(64,filesize,64),unit="Bytes",unit_divisor=64,desc=f"Sending [{fname}]",colour= 'green'):
                bytes_read = f.read(64)
                s.send(bytes_read)
                if filesize-i < 64 :
                    bytes_read = f.read(filesize-i)
                    s.send(bytes_read)
            break
