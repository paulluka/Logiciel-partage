# coding: utf-8

import socket, os, subprocess, pickle, codecs
from tkinter import *
from tkinter.filedialog import *


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
	"""
		Envoie des identifiants et recup de la reponse
		renvoie un booléen pour savoir si on continue ou non
	"""
	global server, connectivity,echec_connection, output_str

	username = get_username()
	password = get_password()

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
		connectivity = True # True -> on peut continuer

	elif log_state[0] == "Fail": # La liste contient le mot clef "Fail" -> on est pas auth.
		print("Le serveur indique : {}".format(log_state[1]))

		echec_connection = Tk()
		echec_connection.title('Echec de la connexion')
		label_echec = Label(echec_connection, text="Le serveur indique : {}".format(log_state[1])).grid(row=0, column=0)
		button_quit = Button(echec_connection, text="quitter", command=destroy_auth_error).grid(row=1, column=1)


		connectivity = False # False -> on est déconnécté

def download():
	"""
		Donne au serveur l'ordre d'envoyer un fichier
	"""
	global server
	folder = str(get_folder())
	filename = str(get_filename())
	print(folder)

	# on crée le chemin absolue
	path = "partage/"+folder +"/"+filename
	print(path)
	data = ["download", path]
	#on dump la liste
	data = pickle.dumps(data)
	server.send(data)

	content = server.recv(2**30) # Reception du conenue du fichier

	if content == b"unknown":
		print("Fichier inéxistant")
	else:
		with open(filename, "wb") as f: # Creation d'un fichier similaire
			print(content)
			f.write(content)
			f.close()

def upload():
	"""
	"""
	global server
	path, target = get_upload_path()
	path_split = path.split('/')
	filename = path_split[-1]
	data = ["upload", filename, 0, target]
	print(path, target, filename)
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



# Fonctions pour récuperer les entrés de l'it graphique

def get_username():
	return entry_username.get()

def get_password():
	return entry_password.get()

def get_folder():
	return entry_folder_dl.get()

def get_filename():
	return entry_filename.get()

#En cas d'erreur, détruire toute les fenetres

def destroy_auth_error():
	echec_connection.destroy()
	interface_client.destroy()

def destroy_download_error():
	pass
		
def arbo():
	arbo_window = Tk()
	label_arbo = Label(arbo_window, text=output_str).grid(row=0, column=0)
	arbo_window.mainloop()

def get_upload_path():
	path = askopenfilename()
	target = entry_folder.get()
	return path, target


if __name__ == "__main__":

	interface_client = Tk()
	interface_client.geometry("400x400")
	interface_client.title("Logiciel de partage")
	#On se connecte au server
	server = connection("localhost", 9999)

	# En tete d'authentification
	
	# Menu
	menubar = Menu(interface_client)
	menubar.add_command(label="Arbo", command=arbo)
	interface_client.config(menu=menubar)
	#Label frame
	label_frame_auth = LabelFrame(interface_client, text="Authentification", padx=20, pady=10, height=200)
	label_frame_auth.grid(row=0, column=0)
	# Nom d'utilisateur
	label_username = Label(label_frame_auth, text="Nom d'utilisateur : ").grid(row=0, column=0)
	entry_username = Entry(label_frame_auth)
	entry_username.grid(row=1, column=0)

	# mot de passe
	label_password = Label(label_frame_auth, text="mot de passe : ").grid(row=0, column=1)
	entry_password = Entry(label_frame_auth)
	entry_password.grid(row=1, column=1)

	# boutton connection
	button_auth = Button(label_frame_auth, text="connection", command=auth).grid(row=1, column=3)


	# CREATIONS WIDGETS UPLOAD / DOWNLOAD

	# Command Frame
	command_frame = Frame(interface_client, borderwidth=5, relief=GROOVE, width=300, height=550)
	command_frame.grid(row=2, column=0)
	#download 

	label_download = Label(command_frame, text="Télécharger").grid(row=0, column=0)
	
	label_folder = Label(command_frame, text="Dossier").grid(row=0, column=1)

	entry_folder_dl = Entry(command_frame)
	entry_folder_dl.grid(row = 1, column = 1)

	label_filename = Label(command_frame, text="Nom du fichier").grid(row=0, column=2)

	entry_filename = Entry(command_frame)
	entry_filename.grid(row = 1, column = 2)

	button_download = Button(command_frame, text="Télécharger", command=download).grid(row=1, column=3)

	# Command Frame
	command_frame = Frame(interface_client, borderwidth=5, relief=GROOVE, width=300, height=550)
	command_frame.grid(row=3, column=0)
	#upload 

	label_upload = Label(command_frame, text="Upload").grid(row=0, column=0)

	label_filename_upload = Label(command_frame, text="dossier cible").grid(row=0, column = 1)

	entry_folder = Entry(command_frame)
	entry_folder.grid(row = 1, column = 1)
	button_download = Button(command_frame, text="Télécharger", command=upload).grid(row=1, column=2)


	interface_client.mainloop()

server.close()
os.system('pause')


