#### Project realised by Henri Gléveau, Tristan Guerin, Théo Le Coz and Grégoire Philippe - INFO A2 ENSIBS
# SecurDoc

A micro-service based program to store file in a Secure way.

## How to start

- Run `pip install -r requirements.txt` to download dependency (You can run `pip install pyzmq` if an error occurs)
- Run `python keyCreation.py` script who creates the keys needed for the communication with the ZMQ server.
- Run `docker-compose up` (Make sure you are using *Docker* and not *Docker Toolbox*, because the specified IP is **localhost**)

(If you want to use it through *Docker Toolbox*, you need to change all the occurrences of **localhost** by
**192.168.99.100** in the *front/APIrequest.js* file)

## How to use 

- Wait for all the dockers to have built

- Open the *front/index.html* page with your web browser (*Firefox* might cause problems)
- You can now navigate through all the pages
    - *Registration* page to register to the website and upload/download files
    - *Connection* page to connect to the website
    - *Upload* page to upload files
    - *Download* page to download files you have uploaded (you can only download files of yours)
    - *Disconnect* button to disconnect of the website