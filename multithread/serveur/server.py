# coding: utf-8 

import socket, threading, subprocess, os, pickle


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
            print("{} Tessaye de s'authentifier avec {}".format((self.ip, self.port), id_))

            # Validité des identifiants
            if id_ == ["paul","luap"]:
                cmd = subprocess.Popen("dir * /s/p", shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                output_bytes = cmd.stdout.read() + cmd.stderr.read()
                # On met dans une liste le mot clef et l'arbo qu'on dump
                log_state = ["Success", output_bytes]
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
            data = client.recv(2**30)
            data = pickle.loads(data)

            if data[0] == "download": # Si l'instruction est "Download"
                print("{} is downloading".format((self.ip, self.port)))
                try:
                    #on ouvre le fichier et on envoie les donnés
                    with open(data[1], "rb") as f:
                        print(data[1])
                        content = f.read()
                        f.close()
                        print(content)
                        client.send(content)
                        print("fichier copié")
                except:
                    content = "unknown"
                    content = content.encode()
                    client.send(content)

            elif data[0] == "upload": # SI l'ordre es "upload"
                path = "partage/" + data[3] + data[1]
                with open(path, "wb") as f: # On ouvre un fichier avec le bon nom
                    f.write(data[2])
                    f.close()
            print("{} a envoyé {}".format((self.ip, self.port), data[1]))





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

