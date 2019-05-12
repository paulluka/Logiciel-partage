#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  serveur.py
#  Paul Lukasiewicz et Ilyess Boussif


import socket, threading, subprocess, os, pickle, json
from chiffrement import *


#Créer une classe qui hérite de Threading
class ClientThread(threading.Thread):


    #Foction qui crée la connection
    def __init__(self, ip, port, clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port))

    #Fonction qui éxécute les taches
    def run(self):

        def auth(client):
            """
                Connection grace a un id et un mdp
                renvoie un booléen pour savoir si on doit continuer ou non
            """
            # On dé-dump la liste
            id_ = client.recv(2048)
            id_ = pickle.loads(id_)
            print("{} essaye de s'authentifier avec {}".format((self.ip, self.port), id_))

            def test_log(id):
                """
                    parcours le fichier log.json a la recherche d'un login et un mdp correspondant a ceux entrés
                    variable "levier" state pour confirmer la connection 
                """
                global state, username
                state = False
                encrypt_mdp = Crypto(id_[1], 9).encrypt_string() #Encrypt le mdp reçue et vois si c'est le même que dans le log
                with open('log.json', "r") as f: #ouverture du fichier    
                    data = json.load(f)
                    try:          
                        if data[str(id_[0])] == encrypt_mdp:
                            state = True # Bon id et mdp
                            username = str(id_[0])
                        else:
                            state = False #Faux id et mdp
                    except:
                        state = False



            test_log(id_)
            # Validité des identifiants
            if state == True:
                # On met dans une liste le mot clef et l'arbo qu'on dump
                log_state = ["Success"]
                log_state = pickle.dumps(log_state)
                client.send(log_state) # Envoie de la réponse
                print("{} authentifié avec {}".format((self.ip, self.port), id_))
                return True # True -> On peux continuer
            else:
                # On met dans une liste le mot clef et la reponse qu'on dump
                log_state = ["Fail", "Echec de la connection vers le serveur"]  
                log_state = pickle.dumps(log_state) 
                client.send(log_state) # On envoie
                print("{} : Echec d'authentification avec {}".format((self.ip, self.port), id_))
               	return False # False -> le client est deconnécté

        def order(client):
            """
                Recoie un ordre du client, cet ordre est donnée par data[0]
            """
            # On recup la list qui contient l'instruction

            data = client.recv(2**15)
            data = pickle.loads(data)

            if data[0] == "download": # Si l'instruction est "Download"
                print("{} is downloading".format((self.ip, self.port)))
                try:
                    #on ouvre le fichier et on envoie les donnés
                    with open(data[1], "rb") as f:
                        content = f.read()
                        f.close()
                    #encrypted_string = Crypto(content,72)
                    #content = encrypted_string.decrypt_string()
                    client.send(content)
                    print("fichier copié")
                except:
                    content = "unknown"
                    content = content.encode()
                    client.send(content)
                    print("{} impossible de trouver {}".format((self.ip, self.port), data[1]))

            elif data[0] == "upload": # Si l'ordre est "upload"
                path = "partage/" + data[3]+"/"+ data[1]
                print(data[2])
                #clear_file = Crypto(data[2] ,72 )
                #clear = clear_file.encrypt_string()
                with open(path, "wb") as f:
                	f.write(data[2])
                	f.close()
                print('Fichier crypté')
                print("{} a envoyé {}".format((self.ip, self.port), data[1]))
                

            elif data[0] == "add_acc":
                if username == "Admin":
                    with open("log.json", "r", encoding="utf-8") as f:
                        logs = json.load(f)
                        encrypt_mdp = Crypto(data[2], 9).encrypt_string()
                        logs[str(data[1])] = encrypt_mdp                       
                        f.close()
                    with open("log.json", "w", encoding="utf-8") as f:
                        json.dump(logs, f, ensure_ascii=False)
                        f.close()
					print("ok acc")
                else:
                    print("Opération refusée")

            elif data[0] == "arbo":
                cmd = subprocess.Popen("dir * /s/p", shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                output_bytes = cmd.stdout.read() + cmd.stderr.read()
                # On met dans une liste le mot clef et l'arbo qu'on dump
                arbo = [output_bytes]
                arbo = pickle.dumps(arbo)
                client.send(arbo) # Envoie de la réponse




        if __name__ == "__main__":
            connectivity = auth(self.clientsocket) # On regarde la valeure du booléen pr savoir si on continue ou non
            if connectivity == False: # On est deco
                print("[+] Déconnexion de {}".format(self.ip))
                self.clientsocket.close()
            else: # On continue
                while True:
                    order(self.clientsocket)

        print("[+] Déconnexion de {}".format(self.ip))
        self.clientsocket.close()

#On creer la connection comme un socket normale
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(("",9999))


#On ecoute et on creer un thread pour chaque conection
while True:
    tcpsock.listen(10)
    print( "En écoute...")
    (clientsocket, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()

