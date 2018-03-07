##########################
# Import de librairie(s) #
##########################

from socket import *

######################
# Paramètres globaux #
######################

# Pour la fonction getPortNumber()
# -- variable r = réponse du serveur
r=''
# -- variable i = compteur de caractères
i=0

# Paramètres de connexion

serverName = '172.16.161.200'
serverPort = 21

#############
# Fonctions #
#############

# *** AMELIORATIONS POSSIBLES ***

def caractereSuivant() :
    global r
    global i

    i=i+1
    return(r[i])

def avanceJusque(d) :
    global r
    global i

    c=caractereSuivant()
    while (c != d) :
        c=caractereSuivant()

def enregistreJusque(d) :
    global r
    global i

    p=''
    c=caractereSuivant()
    while (c != d) :
        p=p+c
        c=caractereSuivant()
    return p

def getPortNumber() :
    global i
    global r

    avanceJusque(',')
    avanceJusque(',')
    avanceJusque(',')
    avanceJusque(',')

    p1=enregistreJusque(',')
    p2=enregistreJusque(')')

    numport=int(p1)*256+int(p2)

    return numport

###################
# Corps du script #
###################


# Etablissement de la connexion de contrôle avec le serveur

clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

# Connexion en tant qu'utilisateur anonyme

#debug
reply = clientSocket.recv(4096)
print(reply)

message = 'USER anonymous\r\n'
clientSocket.send(message.encode('utf-8'))

#debug
reply = clientSocket.recv(4096)
print(reply)

message = 'PASS anonymous@example.com\r\n'
clientSocket.send(message.encode('utf-8'))

#debug
reply = clientSocket.recv(4096)
print(reply)

# Passage en mode passif, extraction du numéro de port à employer

message = 'PASV\r\n'
clientSocket.send(message.encode('utf-8'))
while True:
    r = clientSocket.recv(1024).decode()
    print('boucle')
    if 'Entering Passive Mode' in r:
        #debug
        print('coucou '+r)
        break

port = getPortNumber()

#debug
print('numero de port: '+port)

# Etablissement de la connexion de données avec le serveur
cs = socket(AF_INET,SOCK_STREAM)
cs.connect((serverName, port))

# Demande du fichier

message = 'RETR coucou.txt\r\n'
clientSocket.send(message.encode('utf-8'))

# Réception (réponses du serveur et données)

reply = cs.recv(65535).decode()
print(reply)

# Fermeture de la connexion de contrôle (celle de données est fermée par le serveur à la fin du tranfert)

cs.close()
clientSocket.close()
