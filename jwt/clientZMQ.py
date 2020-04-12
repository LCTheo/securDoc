# -*- coding: utf-8 -*-

#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to client, expects "World" back
#
import time
import zmq.auth
import zmq
import shutil
import os
from zmq.auth.thread import ThreadAuthenticator
import sys



#################################################################
#
# create keyfile on keyClient directory
#
#################################################################
def createKey(Directoryname,filename) :
	keys_dir = os.path.join(os.path.dirname(__file__), Directoryname)
	os.system("mkdir "+ Directoryname+" 2> /dev/null")

	# create new keys in key dir
	#client_public_file, client_secret_file = zmq.auth.create_certificates(keys_dir, "client")

	client_public_file, client_secret_file = zmq.auth.create_certificates(keys_dir, filename)


#################################################################
#
# deletekeyClient directory
#
#################################################################
def deleteKey(Directoryname) : 
	os.system("rm -r " +Directoryname+"2> /dev/null")

#################################################################
#
# initiate a socket to send information
# ctx, the zmq context
# port, the port to send
# path_privateKey, the path to access at the private key
#
#################################################################
def initSend(ctx,port,path_privateKey) : 
	serverSend = ctx.socket(zmq.PUSH)

	# get the directory where the keys are.
	base_dir = os.path.dirname(__file__)
	server_secret_file = os.path.join(base_dir,path_privateKey)

	# get the file of server certificat.
	server_public, server_secret = zmq.auth.load_certificate(server_secret_file)
	
	# give the certificat.
	serverSend.curve_secretkey = server_secret
	serverSend.curve_publickey = server_public

	# bind the server send socket
	serverSend.curve_server = True  # must come before bind
	serverSend.bind('tcp://*:'+str(port))
	return serverSend


#################################################################
#
# initiate a socket to receive information
# ctx, the zmq context
# port, the port to receive
# path_privateKey, the path to access at the private key
# path_publicKey, the path to access at the public key of the client
# ipServer, ip of server
#
#################################################################
def initReceive(ctx,port,path_privateKey,path_publicKey,ipServer) :
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
	serverReceive.connect("tcp://"+ipServer+":"+str(port))
	return serverReceive


#################################################################
#
# send id and pass to a server to receive a token
# portSend, the to send data
# portReceive, the port to receive
# clientSecretKey, the path to access at the private key
# serverPublicKey, the path to access at the public key of the server
# ID, ID to save in the token
# hash_pass, pass to save in the token
#
#################################################################
def needToken(portSend,portReceive,clientSecretKey,serverPublicKey,ipServer, ID,hash_pass):
	# create context for socket
	ctx = zmq.Context.instance()

	# init client to send data
	clientSend = initSend(ctx,portSend,clientSecretKey)
	# init client to receive data
	clientReceive = initReceive(ctx,portReceive,clientSecretKey,serverPublicKey, ipServer)

	# send string
	clientSend.send_string(ID+" "+hash_pass)

	# read response
	a=0
	while True :
		if clientReceive.poll(1000):
			res = clientReceive.recv_string()
			return res


#################################################################
#
# send token to a server and read response
# portSend, the to send data
# portReceive, the port to receive
# clientSecretKey, the path to access at the private key
# serverPublicKey, the path to access at the public key of the server
# token, the token to verif
#
#################################################################
def verifToken(portSend,portReceive,clientSecretKey,serverPublicKey,ipServer,token):
	# A CLIENT WHO NEED TO VERIF TOKEN
	ctx = zmq.Context.instance()
	# create other socket to send and receive data
	clientSend2 = initSend(ctx,portSend,clientSecretKey)
	clientReceive2 = initReceive(ctx,portReceive,clientSecretKey,serverPublicKey,ipServer)

	# send login and my token
	clientSend2.send_string("login "+token)

	# read response
	while True :
		if clientReceive2.poll(1000):
			res = clientReceive2.recv_string()
			return res


def exchangeKey(ipServer,portServer,serverKeyDirectory,clientPublicKey,ID):
	context = zmq.Context()
	socket = context.socket(zmq.REQ)
	socket.connect("tcp://"+ipServer+":"+portReceive)

	g.open(clientPublicKey,"r")
	publickey=g.read()
	g.close()
	
	socket.send_string(ID+":::"+publickey)

	while True :
	    message = socket.recv_string()
	    f=open(serverKeyDirectory+"/server.key","w+")
    	f.write(message)
    	f.close()
    	exit()
	 


################################################################################


if __name__ == "__main__":
	if (len(sys.argv[1:])<1):
		print("wrong argument")
		exit()
	fonction = sys.argv[1]
	if(fonction=="key" and len(sys.argv[1:])==3) :
		createkey(sys.argv[2],sys.argv[3])
		exit()
	if(fonction=="deleteKey" and len(sys.argv[1:])==2):
		deleteKey(sys.argv[2])
		exit()
	if (len(sys.argv[1:])==8 and sys.argv[1]=="needToken") :
		needToken(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7],sys.argv[8])
		exit()
	if (len(sys.argv[1:])==7 and sys.argv[1]=="verifToken") :
		verifToken(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7])
		exit()
	if (len(sys.argv[1:])==6 and sys.argv[1]=="exchangeKey") :
		exchangeKey(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])
		exit()
	print("wrong argument")
	exit()
################################################################################




