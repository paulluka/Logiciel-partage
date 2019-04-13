# coding: utf-8

import socket, os, subprocess, pickle, codecs


def connection(hote, port):

	connection_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		connection_server.connect((hote, port))
	except:
		print("[*] Hôte inéxistant ")
		os.system("pause")
		os.system("exit")
	return connection_server

def auth(server):
	"""
		Envoie des identifiants et recup de la reponse
		renvoie un booléen pour savoir si on continue ou non
	"""
	global username
	username = input("Nom d'utilisateur : ")
	password = input("Mot de passe : ")

	# On dump la list pour pouvoir l'envoyer a travers le socket
	id_ = [username, password]
	id_dump = pickle.dumps(id_)
	server.send(id_dump)
	#On recupere une listeen retour qu'on dé-dump
	log_state = server.recv(2048)
	log_state = pickle.loads(log_state)

	if log_state[0] == "Success": # La liste contient le mot clef "Success" -> on est auth.
		print("{} a autorisé une connection".format(server))
		# On récup l'arbo
		codecs.register_error('replace_with_space', lambda e: (u'',e.start + 1)) # On remplace les potentiels erreurs par des espaces
		output_str = log_state[1].decode("utf-8", errors='replace_with_space')
		print(output_str) # On affiche l'arbo
		return True # True -> onpeut continuer
	elif log_state[0] == "Fail": # La liste contient le mot clef "Fail" -> on est pas auth.
		print("Le serveur indique : {}".format(log_state[1]))
		return False # False -> on est déconnécté

def download(server):
	"""
		Donne au serveur l'ordre d'envoyer un fichier
	"""

	folder = input("chemin du fichier a télécharger : ")
	filename = input("Nom du fichier : ")
	# on crée le chemin absolue
	path = "partage/"+folder +"/"+filename
	data = ["download", path]
	#on dump la liste
	data = pickle.dumps(data)
	server.send(data)

	content = server.recv(2**30) # Reception du conenue du fichier

	if content == b"unknown":
		print("Fichier inéxistant")
		os.system("pause")
	else:
		with open(filename, "wb") as f: # Creation d'un fichier similaire
			f.write(content)
			f.close()

def upload(server):
	"""
	"""

	folder = "à envoyer"
	filename = input("Nom du fichier : ")
	target = input("chemin du dossier cible : ")
	# on crée le chemin absolue

	path = folder +"/"+filename
	data = ["upload", filename, 0, target]
	print(path)
	# On verifie que le fichier existe
	try:
		with open(path, "rb") as f:
			content = f.read()
			data[2] = content
			
		#on dump la liste
		data = pickle.dumps(data)
		server.send(data)
		print("Le fichier a été copié avec succès")
	except:
		print("Le fichier n'éxiste pas .")

def add_acc(server):
	""" Creer un compte """


	new_username = input("Nom d'utilisateur : ")
	comf_password, new_password = 1, 2
	while comf_password != new_password:
		new_password = input("Mot de passe : ")
		comf_password = input("comfirmez le mot de passe : ")
	data = ["add_acc", new_username, new_password]
	data = pickle.dumps(data)
	server.send(data)
	print("Compte créé")


	




if __name__ == "__main__":
	#On se connecte au server
	server = connection("127.0.0.1", 9999)
	connectivity = auth(server) # On regarde la valeure du booléen pr savoir si on continue ou non
	if connectivity == True: # On continue
		stop = False # Variable qui limite la boucle jusqu'a ce que l'onchoisisse de quitter
		while stop != True:
			menu = """
			1 - Télécharger un fichier
			2 - Uploader un fichier
			3 - quitter

					"""
			print(menu)
			choice = int(input("Choisissez une option(1, 2 ou 3) : "))
			if choice == 1:
				download(server)
			elif choice == 2:
				upload(server)
			elif choice == 3:
				stop = True
			elif choice == 42:
				if username == "Admin":
					add_acc(server)
				else:
					print("Accès interdit")
			else:
				pass
	elif connectivity == False: # On est deco
		server.close()

server.close()



	

os.system('pause')


