#### Project realised by Henri Gléveau, Tristan Guerin, Théo Le Coz and Grégoire Philippe - INFO A2 ENSIBS
# SecurDoc

A micro-service based program to store file in a Secure way.

## How to setup

- Run `pip install -r requirements.txt` to download dependency (You can run `pip install pyzmq` if an error occurs)
- Run `python keyCreation.py` script who creates the keys needed for the communication with the ZMQ server.
- You can change the password variable `JWT_PASS` and `DOC_PASS` in the docker-compose.yml if you want
- If you use a different setup of *Docker* like *Docker Toolbox* or remote docker server, change the `dockerIP` variable in the *front/APIrequest.js* file

## How to start 
- Run `docker-compose up`
- Wait for all the dockers to have built

- Open the *front/index.html* page with your web browser (*Firefox* might cause problems)
- You can now navigate through all the pages
    - *Registration* page to register to the website and upload/download files
    - *Connection* page to connect to the website
    - *Upload* page to upload files
    - *Download* page to download files you have uploaded (you can only download files of yours)
    - *Disconnect* button to disconnect of the website