# -*- coding: utf-8 -*-

import datetime
import zmq
import zmq.auth
import os
import jwt
from threading import Thread
import sys
import logging


#################################################################
#
# create public and private key
# directoryname, le répertoire à creer pour stocker les clés
# filename, le nom des clés.
#
#################################################################
def createKey(directoryname, filename):
    keys_dir = os.path.join(os.path.dirname(__file__), directoryname)
    os.system("mkdir " + directoryname + " 2> /dev/null")
    server_public_file, server_secret_file = zmq.auth.create_certificates(keys_dir, filename)


#################################################################
#
# delete the directory where the keys are stored
# directoryname, the name oh the directory 
#
#################################################################
def deleteKey(directoryname):
    os.system("rm -r " + directoryname)


#################################################################
#
# initiate a socket to send information
# ctx, the zmq context
# port, the port to send
# path_privateKey, the path to access at the private key
# filename, curent directory
#
#################################################################
def initSend(ctx, port, path_privateKey, filename):
    serverSend = ctx.socket(zmq.PUSH)

    # get the directory where the keys are.
    base_dir = filename
    server_secret_file = os.path.join(base_dir, path_privateKey)

    # get the file of server certificat.
    server_public, server_secret = zmq.auth.load_certificate(server_secret_file)

    # give the certificat.
    serverSend.curve_secretkey = server_secret
    serverSend.curve_publickey = server_public

    # bind the server send socket
    serverSend.curve_server = True  # must come before bind
    serverSend.bind('tcp://*:' + str(port))
    return serverSend


#################################################################
#
# initiate a socket to receive information
# ctx, the zmq context
# port, the port to receive
# path_privateKey, the path to access at the private key
# path_publicKey, the path to access at the public key of the client
# filename, curent directory
# ip, ip of client
#
#################################################################
def initReceive(ctx, port, path_privateKey, path_publicKey, filename, ip):
    serverReceive = ctx.socket(zmq.PULL)

    # get the directory where the keys are.
    base_dir = filename

    # get the file of server certificat.
    server_secret_file = os.path.join(base_dir, path_privateKey)
    server_public, server_secret = zmq.auth.load_certificate(server_secret_file)

    # give the certificat.
    serverReceive.curve_secretkey = server_secret
    serverReceive.curve_publickey = server_public

    # give the public key of client to communicate with him.
    client_public_file = os.path.join(base_dir, path_publicKey)
    client_public, _ = zmq.auth.load_certificate(client_public_file)
    serverReceive.curve_serverkey = client_public

    # connect the server receive socket
    serverReceive.connect("tcp://" + ip + ":" + str(port))
    return serverReceive


class ThreadVerifToken(Thread):

    #################################################################
    #
    # init the thread who have to verif token
    # ctx, the zmq context
    # portReceive, the port to receive data
    # portSend, the port to send data
    # serversecretkeyfile, server secret key file
    # clientpublickeyfile, client public key file
    # secretkey, secret to encode/decode token
    # filename, the current directory
    # ipClient, ip of client
    #
    #################################################################
    def __init__(self, ctx, portReceive, portSend, serversecretkeyfile, clientpublickeyfile, secretkey, filename,
                 ipClient):
        Thread.__init__(self)
        self.ctx = ctx
        self.portReceive = portReceive
        self.portSend = portSend
        self.filename = filename
        self.serversecretkeyfile = serversecretkeyfile
        self.clientpublickeyfile = clientpublickeyfile
        self.secretkey = secretkey
        self.ipClient = ipClient

    #################################################################
    #
    # run my thread, create two socket. One to read data with authentificated client
    # and on other to send data
    #
    #################################################################
    def run(self):
        serverSend = initSend(self.ctx, self.portSend, self.serversecretkeyfile, self.filename)
        serverReceive = initReceive(self.ctx, self.portReceive, self.serversecretkeyfile, self.clientpublickeyfile,
                                    self.filename, self.ipClient)
        mes = ""
        while True:
            if serverReceive.poll(1000):
                msg = serverReceive.recv_string()
                logging.info('verif : ' + msg)
                isvalid = self.tokenValid(msg, self.secretkey)
                logging.info('verif isvalid: ' + str(isvalid))
                serverSend.send_string(str(isvalid))

    #################################################################
    #
    # test is token is valid
    # payload, text argument compose of client id and one token
    # secret, secret key to decode token
    #
    #################################################################
    def tokenValid(self, payload, secret):
        tab = payload.split(' ')
        token = tab[1]
        ID = tab[0]
        try:
            payload = jwt.decode(token, secret, algorithms=['HS256'])
            print(payload)
            if payload['id'] != ID:
                return False
            else:
                return True
        except:
            return False


class ThreadCreateToken(Thread):

    #################################################################
    #
    # init the thread who have to create token
    # ctx, the zmq context
    # portReceive, the port to receive data
    # portSend, the port to send data
    # serversecretkeyfile, server secret key file
    # clientpublickeyfile, client public key file
    # secretkey, secret to encode/decode token
    # filename, the current directory
    # ipClient, ip of client
    #
    #################################################################
    def __init__(self, ctx, portReceive, portSend, serversecretkeyfile, clientpublickeyfile, secretkey, filename,
                 ipClient):
        Thread.__init__(self)
        self.ctx = ctx
        self.portReceive = portReceive
        self.portSend = portSend
        self.serversecretkeyfile = serversecretkeyfile
        self.clientpublickeyfile = clientpublickeyfile
        self.secretkey = secretkey
        self.filename = filename
        self.ipClient = ipClient

    #################################################################
    #
    # run my thread, create two socket. One to read data with authentificated client
    # and on other to send data
    #
    #################################################################
    def run(self):
        serverSend = initSend(self.ctx, self.portSend, self.serversecretkeyfile, self.filename)
        serverReceive = initReceive(self.ctx, self.portReceive, self.serversecretkeyfile, self.clientpublickeyfile,
                                    self.filename, self.ipClient)
        mes = ""
        while True:
            if serverReceive.poll(1000):
                msg = serverReceive.recv_string()
                logging.info('create : ' + msg)
                serverSend.send_string(str(self.createJWT(msg, self.secretkey)))

    #################################################################
    #
    # create jwt token
    # payload, a text argument composed of login and password
    # secret, the secretkey
    #
    #################################################################
    def createJWT(self, payload, secret):
        tab = payload.split(' ')
        ID = tab[0]
        hash_password = tab[1]
        payload = {'id': ID, 'hash_password': hash_password,
                   'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)};
        token = jwt.encode(payload, secret, algorithm='HS256')
        return token


def exchangePublicKey(port, clientKeyDirectory, serverPublicKey):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:" + str(port))

    g = open(serverPublicKey, "r")
    publickey = g.read()
    g.close()
    while True:
        #  Wait for next request from client
        message = socket.recv_string()
        tab = message.split(':::')
        f = open(clientKeyDirectory + "/" + tab[0] + ".key", "w+")
        f.write(tab[1])
        f.close()
        socket.send_string(publickey)


#################################################################
#
# main fonction to listen and send information about token
#
#################################################################
def main(portReceiveCreate, portSendCreate, portReceiveVerif, portSendVerif, privateKeyServer, publicKeyClientCreate,
         publicKeyClientVerif, ipClientCreate, ipClientVerif, secret):
    logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    logging.info('start')
    ctx = zmq.Context.instance()
    t = ThreadVerifToken(ctx, portReceiveVerif, portSendVerif, privateKeyServer, publicKeyClientVerif, secret,
                         os.path.dirname(__file__), ipClientVerif)
    t.start()
    v = ThreadCreateToken(ctx, portReceiveCreate, portSendCreate, privateKeyServer, publicKeyClientCreate, secret,
                          os.path.dirname(__file__), ipClientCreate)
    v.start()


################################################################################

if __name__ == "__main__":
    if len(sys.argv[1:]) < 1:
        print("wrong argument")
    else:
        fonction = sys.argv[1]
        if fonction == "key" and len(sys.argv[1:]) == 3:
            createKey(sys.argv[2], sys.argv[3])

        elif fonction == "deleteKey" and len(sys.argv[1:]) == 2:
            deleteKey(sys.argv[2])

        elif len(sys.argv[1:]) == 11 and fonction == "main":
            main(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9],
                 sys.argv[10], sys.argv[11])

        elif fonction == "exchangeKey" and len(sys.argv[1:]) == 4:
            exchangePublicKey(sys.argv[2], sys.argv[3], sys.argv[4])
