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
    public_key_file, secret_key_file = zmq.auth.create_certificates(keys_dir, filename)
    return public_key_file


#################################################################
#
# delete the directory where the keys are stored
# directoryname, the name oh the directory
#
#################################################################
def deleteKey(directoryname):
    os.rmdir(directoryname)


if __name__ == "__main__":
    if path.exists("jwt/keyServer"):
        deleteKey("jwt/keyServer")
    public_serv_key = createKey("jwt/keyServer", "server")
    if path.exists("jwt/keyClient"):
        deleteKey("jwt/keyClient")
    os.mkdir("jwt/keyClient")

    if path.exists("rsc/keyClient"):
        deleteKey("rsc/keyClient")
    public_client_key = createKey("rsc/keyClient", "client")
    if path.exists("rsc/keyServer"):
        deleteKey("rsc/keyServer")
    os.mkdir("rsc/keyServer")

    if path.exists("rsc/keyClient"):
        deleteKey("rsc/keyClient")

    if path.exists("rsc/keyServer"):
        deleteKey("rsc/keyServer")
