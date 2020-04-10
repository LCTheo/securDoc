# -*- coding: utf-8 -*-

#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to client, expects "World" back
#
import zmq.auth
import zmq
import os


def getToken(user_id, hash):
    # create context for socket
    ctx = zmq.Context.instance()

    # init client to send data
    clientSend = initSend(ctx, 5555, "keyClient/client.key_secret")
    # init client to receive data
    clientReceive = initReceive(ctx, 5556, "keyClient/client.key_secret", "keyServer/server.key")

    # send string
    clientSend.send_string(user_id+" hash_pass")

    # read response
    a = 0
    while a == 0:
        if clientReceive.poll(1000):
            res = clientReceive.recv_string()
            return res


#################################################################
#
# create keyfile on keyClient directory
#
#################################################################
def createKey():
    keys_dir = os.path.join(os.path.dirname(__file__), 'keyClient')
    os.mkdir("keyClient")

    # create new keys in key dir
    # client_public_file, client_secret_file = zmq.auth.create_certificates(keys_dir, "client")

    client_public_file, client_secret_file = zmq.auth.create_certificates(keys_dir, "client")


#################################################################
#
# deletekeyClient directory
#
#################################################################
def deleteKey():
    os.system("rm -r keyClient")


#################################################################
#
# deletekeyClient directory
#
#################################################################
def initSend(ctx, port, path_privateKey):
    serverSend = ctx.socket(zmq.PUSH)

    # get the directory where the keys are.
    base_dir = os.path.dirname(__file__)
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
# deletekeyClient directory
#
#################################################################
def initReceive(ctx, port, path_privateKey, path_publicKey,):
    serverReceive = ctx.socket(zmq.PULL)

    # get the directory where the keys are.
    base_dir = os.path.dirname(__file__)

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
    serverReceive.connect("tcp://jwt:" + str(port))
    return serverReceive