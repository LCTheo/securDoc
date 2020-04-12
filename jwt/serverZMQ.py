import datetime
import zmq.auth
import zmq
import os
import jwt
from threading import Thread


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
#
#################################################################
def initReceive(ctx, port, path_privateKey, path_publicKey, filename):
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
    serverReceive.connect("tcp://localhost:" + str(port))
    return serverReceive


class ThreadVerifToken(Thread):

    #################################################################
    #
    # init the thread who have to verif token
    # ctx, the zmq context
    # portReceive, the port to receive data
    # portSend, th eport to send data
    # filename, the current directory
    #
    #################################################################
    def __init__(self, ctx, portReceive, portSend, filename):
        Thread.__init__(self)
        self.ctx = ctx
        self.portReceive = portReceive
        self.portSend = portSend
        self.filename = filename

    #################################################################
    #
    # run my thread, create two socket. One to read data with authentificated client
    # and on other to send data
    #
    #################################################################
    def run(self):
        serverSend = initSend(self.ctx, self.portSend, "keyServer/server.key_secret", self.filename)
        serverReceive = initReceive(self.ctx, self.portReceive, "keyServer/server.key_secret", "keyClient/client.key",
                                    self.filename)
        mes = ""
        while True:
            if serverReceive.poll(1000):
                msg = serverReceive.recv_string()
                print(msg)
                isvalid = self.tokenValid(msg, 'secretkeyfortoken')
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
    # portSend, th eport to send data
    # filename, the current directory
    #
    #################################################################
    def __init__(self, ctx, portReceive, portSend, filename):
        Thread.__init__(self)
        self.ctx = ctx
        self.portReceive = portReceive
        self.portSend = portSend
        self.filename = filename

    #################################################################
    #
    # run my thread, create two socket. One to read data with authentificated client
    # and on other to send data
    #
    #################################################################
    def run(self):
        serverSend = initSend(self.ctx, self.portSend, "keyServer/server.key_secret", self.filename)
        serverReceive = initReceive(self.ctx, self.portReceive, "keyServer/server.key_secret", "keyClient/client.key",
                                    self.filename)
        mes = ""
        while True:
            if serverReceive.poll(1000):
                msg = serverReceive.recv_string()
                print(msg)
                print(self.createJWT(msg, 'secretkeyfortoken'))
                serverSend.send_string(self.createJWT(msg, 'secretkeyfortoken'))

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


################################################################################

ctx = zmq.Context.instance()

t = ThreadVerifToken(ctx, 5557, 5558, os.path.dirname(__file__))
t.start()

v = ThreadCreateToken(ctx, 5555, 5556, os.path.dirname(__file__))
v.start()

# deleteKey()
