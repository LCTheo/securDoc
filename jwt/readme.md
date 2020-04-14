### Lancement script ###


|*************************|
|** Server serverZMQ.py **|
|*************************|

1) fonction création de clé : 

python serverZMQ.py key <directory> <name>

-directory : repertoire où stocker les clés ( existant ou non)
-name : le nom à attribuer au fichier contenant les clés.

------------------------------------------------------------------

2) fonction destruction de clé : 

python serverZMQ.py deleteKey <directory>

-directory : repertoire à suprimer

------------------------------------------------------------------

3) fonction d'échange de clés :

python serverZMQ.py exchangeKey <port> <clientKeyDirectory> <serverPublicKey>

-port : port d'écoute du serveur pour l'échange de clé
-clientKeyDirectory : répertoire où stocker les clés clients récupérer
-serverPublicKey : la clé public du serveur à envoyer

------------------------------------------------------------------

4) fonction principale de création et de vérification de jeton

python serverZMQ.py main <portReceiveCreate> <portSendCreate> <portReceiveVerif> <portSendVerif> <privateKeyServer> <publicKeyClientCreate> <publicKeyClientVerif> <IpClientCreate> <IpClientVerif> <secretKey>

-portReceiveCreate : port où recevoir les informations pour la creation de jeton
-portSendCreate : port où ecrire les informations pour la creation de jeton
-portReceiveVerif : port où recevoir les informations pour la vérification de jeton
-portSendVerif : port où ecrire les informations pour la vérification de jeton
-privateKeyServer : fichier contenant la clé privé du server
-publicKeyClientCreate : fichier contenant la clé public du client qui à besion de jeton
-publicKeyClientVerif : fichier contenant la clé public du client qui veut vérifier un jeton
-IpClientCreate : ip du client qui a besion de jeton
-IpClientVerif : ip du client qui veut vérifier un jeton
-secretKey : mot de passe pour dé/chiffrer les jwt

****************************************************************************
****************************************************************************
****************************************************************************

|*************************|
|** Client clientZMQ.py **|
|*************************|

1) fonction création de clé : 

python clientZMQ.py key <directory> <name>

-directory : repertoire où stocker les clés ( existant ou non)
-name : le nom à attribuer au fichier contenant les clés.

------------------------------------------------------------------

2) fonction destruction de clé : 

python clientZMQ.py deleteKey <directory>

-directory : repertoire à suprimer

------------------------------------------------------------------

3) fonction d'échange de clés :

python clientZMQ.py exchangeKey <IpServer> <portServer> <serverKeyDirectory> <clientPublicKey> <ID>

-IpServer : ip du server pour echanger les clés publiques
-portServer : port d'écoute du serveur pour l'échange de clé
-serverKeyDirectory : répertoire où stocker la clé server récupérer
-clientPublicKey : la clé public du client à envoyer
-ID : nom a associer à cette clé

------------------------------------------------------------------

4) fonction de récupération de jeton :

python clientZMQ.py needToken <portSend> <portReceive> <clientSecretKey> <serverPublicKey> <ipServer> <ID> <hash_pass>

-portSend : port d'envoie du client
-portReceive : port de reception du client
-clientSecretKey : fichier de la clé secrete du client
-serverPublicKey : fichier de la clé publique du serveur
-ipServer : ip du serveur
-ID : id associé au mot de passe à stocker dans le jeton
-hash_pass : mot de passe à stocker au jeton

------------------------------------------------------------------ 

5) fonction de vérification de jeton :

python clientZMQ.py verifToken <portSend> <portServer> <clientSecretKey> <serverPublicKey> <ipServer> <token>

-portSend : port d'envoie du client
-portReceive : port de reception du client
-clientSecretKey : fichier de la clé secrete du client
-serverPublicKey : fichier de la clé publique du serveur
-ipServer : ip du serveur
-token : jeton à vérifier

------------------------------------------------------------------














