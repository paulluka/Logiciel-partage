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

def auth():
	global server
	"""
		Envoie des identifiants et recup de la reponse
		renvoie un booléen pour savoir si on continue ou non
	"""

	username = input("Nom d'utilisateur : ")
	password = input("Mot de passe : ")

	# On dump la list pour pouvoir l'envoyer a travers le socket
	id_ = [username, password]
	id_dump = pickle.dumps(id_)
	server.send(id_dump)
	#On recupere une liste en retour qu'on load
	log_state = server.recv(2048)
	log_state = pickle.loads(log_state)

	if log_state[0] == "Success": # La liste contient le mot clef "Success" -> on est auth.
		print("{} a autorisé une connection".format(server))
		# On récup l'arbo
		codecs.register_error('replace_with_space', lambda e: (u'',e.start + 1)) # On remplace les potentiels erreurs par des espaces
		output_str = log_state[1].decode("utf-8", errors='replace_with_space')
		print(output_str) # On affiche l'arbo
		return True # True -> on peut continuer
	elif log_state[0] == "Fail": # La liste contient le mot clef "Fail" -> on est pas auth.
		print("Le serveur indique : {}".format(log_state[1]))
		return False # False -> on est déconnécté

def download():
	global server
	"""
		Donne au serveur l'ordre d'envoyer un fichier
	"""

	folder = input("chemin du fichier a télécharger : ")
	filename = input("Nom du fichier : ")
	# on crée le chemin absolue
	path = folder +"/"+filename
	data = ["download", path]
	#on dump la liste
	data = pickle.dumps(data)
	server.send(data)

	content = server.recv(32768) # Reception du conenue du fichier

	if content == b"unknown":
		print("Fichier inéxistant")
		os.system("pause")
	else:
		with open(filename, "wb") as f: # Creation d'un fichier similaire
			print(content)
			f.write(content)
			f.close()

def upload():
	global server
	"""
	Envoie un fichier au serveur
	"""

	folder = "tosend"
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
	




if __name__ == "__main__":
	#On se connecte au server
	server = connection("172.20.0.113", 9999)

	###
	###DEBUT TKINTER###
	###
	main_window = Tk()
	main_window.geometry("500x500")
	# 




	main_window.mainloop()

	





	

os.system('pause')


