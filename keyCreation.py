import shutil
from os import path
import zmq.auth
import zmq
import os


################################################################
#
# create public and private key
# directoryname, le répertoire à creer pour stocker les clés
# filename, le nom des clés.
#
#################################################################
def createKey(directoryname, filename):
    keys_dir = os.path.join(os.path.dirname(__file__), directoryname)
    os.mkdir(directoryname)
    zmq.auth.create_certificates(keys_dir, filename)


#################################################################
#
# delete the directory where the keys are stored
# directoryname, the name oh the directory
#
#################################################################
def deleteKey(directoryname):
    shutil.rmtree(directoryname)


if __name__ == "__main__":
    if path.exists("jwt/keyServer"):
        deleteKey("jwt/keyServer")
    createKey("jwt/keyServer", "server")
    if path.exists("jwt/keyClient"):
        deleteKey("jwt/keyClient")
    os.mkdir("jwt/keyClient")

    if path.exists("rsc/keyClient"):
        deleteKey("rsc/keyClient")
    createKey("rsc/keyClient", "client")
    shutil.copyfile("rsc/keyClient/client.key", "jwt/keyClient/client.key")
    if path.exists("rsc/keyServer"):
        deleteKey("rsc/keyServer")
    os.mkdir("rsc/keyServer")
    shutil.copyfile("jwt/keyServer/server.key", "rsc/keyServer/server.key")

    if path.exists("usr/keyClient"):
        deleteKey("usr/keyClient")
    shutil.copytree("rsc/keyClient", "usr/keyClient")
    if path.exists("usr/keyServer"):
        deleteKey("usr/keyServer")
    shutil.copytree("rsc/keyServer", "usr/keyServer")
