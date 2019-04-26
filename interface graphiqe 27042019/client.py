
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  client.py
#  Paul Lukasiewicz et Ilyess Boussif

from tkinter import * 
from tkinter.messagebox import *
from tkinter.filedialog import *
import socket, os, subprocess, pickle, codecs

def download_ig():
	"""
		Décrir fonction
	"""
	#Afiichage des labels a la demande du client
	global entry_folder_download, entry_filename_download, label_download #globaliser les variables qu'on utilise a l'exterieur de la fonction
	label_download = Label(frame_choix, text = "Veuillez écrire le nom du fichier que vous voulez télécharger et son dossier: ", bg = 'pink', fg = 'black', font = 15)
	label_download.place(relx = 0.16 , rely = 0.34, relwidth= 0.72, relheight = 0.2)
	
	# Rentrer le nom du dossier désiré
	entry_filename_download = Entry(frame_choix)
	entry_filename_download.place(relx = 0.25 , rely = 0.5, relwidth= 0.3, relheight = 0.09)

	# Rentrer le dossier dans lequel il se touve
	entry_folder_download = Entry(frame_choix)
	entry_folder_download.place(relx = 0.50 , rely = 0.5, relwidth= 0.3, relheight = 0.09)


	Button_Valider_download = Button(frame_choix, text = "Valider", command = download)
	Button_Valider_download.place(relx = 0.36 , rely = 0.6, relwidth= 0.3, relheight = 0.09)

def upload_ig():
	"""
		Décrir fonction
	"""
	#Affichage des labels a la demande du client
	global entry_folder_upload, label_upload #globaliser les variables qu'on utilise a l'exterieur de la fonction
	label_upload = Label(frame_choix, text = "Veuillez écrire le nom du dossier dans lequel vous voulez insérer : ", bg = 'pink', fg = 'black', font = 15)
	label_upload.place(relx = 0.16 , rely = 0.34, relwidth= 0.7, relheight = 0.2)
	# Rentrer le dossier cible
	entry_folder_upload = Entry(frame_choix)
	entry_folder_upload.place(relx = 0.36 , rely = 0.5, relwidth= 0.3, relheight = 0.09)

	Button_Valider_upload = Button(frame_choix, text = "Valider", command = upload)
	Button_Valider_upload.place(relx = 0.36 , rely = 0.6, relwidth= 0.3, relheight = 0.09)

def deconnexion_ig():
	"""
		Décrir fonction
	"""
	#message deco client
	showinfo("Déconnexion", "Vous avez été déconnectés avec succès !")
	root.destroy()


def connection(hote, port):
	"""
		Creer une connection vers le serveur grace a un socket
		return la variable nécéssaire au dialogue
	"""
	connection_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		connection_server.connect((hote, port))
	except:
		showinfo("Serveur", "[*] Hôte inéxistant ")
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
		# On récup l'arbo
		codecs.register_error('replace_with_space', lambda e: (u'',e.start + 1)) # On remplace les potentiels erreurs par des espaces
		output_str = log_state[1].decode("utf-8", errors='replace_with_space')
		connectivity = True # True -> on peut continuer
		frame_deux()
	elif log_state[0] == "Fail": # La liste contient le mot clef "Fail" -> on est pas auth.
		showinfo("Indication", "Le serveur indique : {}".format(log_state[1]))

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
	# recuperer les informations util a l'envoie dans l'interface graphique
	folder = str(get_folder_download())
	filename = str(get_filename())

	# on crée le chemin absolue
	path = "partage/"+folder +"/"+filename
	data = ["download", path] #informations a envoyer au serveur

	#on dump la liste
	data = pickle.dumps(data)
	server.send(data)

	content = server.recv(2**30) # Reception du conenue du fichier

	if content == b"unknown": #gestion d'erreur: si le fichier n'existe pas
		showinfo("Erreur", "Fichier inéxistant")
	else:
		with open(filename, "wb") as f: # Creation d'un fichier similaire
			f.write(content)
			f.close()
		label_download.config(text="Fichier téléchargé")

def upload():
	"""
		Envoie un fichier sur le serveur 
	"""
	global server
	path, target = get_upload_path() #recupere le chemin du fichier et le dossier cible sur le serveur
	filename = path.split('/')[-1] #recupere le nom du fichier contenue dans path
	data = ["upload", filename, 0, target]
	# On verifie que le fichier existe et on l'envoie
	try:
		with open(path, "rb") as f:
			content = f.read()
			data[2] = content
			
		#on dump la liste
		data = pickle.dumps(data)
		server.send(data)
		label_upload.config(text='Fichier envoyé avec succès')
	except:
		showinfo("Envoie", "Le fichier n'éxiste pas ou ne peut pas etre ouvert .")



# Fonctions pour récuperer les entrés de l'it graphique

def get_username():
	return IdEntry.get()

def get_password():
	return MDPEntry.get()

def get_folder_upload():
	return entry_folder_upload.get()
 
def get_filename():
	return entry_filename_download.get()

def get_folder_download():
	return entry_folder_download.get()

#En cas d'erreur, détruire toute les fenetres

def destroy_auth_error():
	echec_connection.destroy()
	root.destroy()

def destroy_download_error():
	pass
		
def arbo():
	arbo_window = Tk()
	label_arbo = Label(arbo_window, text=output_str).grid(row=0, column=0)
	arbo_window.mainloop()

def get_upload_path():
	path = askopenfilename()
	target = get_folder_upload()
	return path, target


if __name__ == "__main__":


	#On se connecte au server
	server = connection("localhost", 9999)

	#################################### Interface graphique ############################################
	HEIGHT = 600
	WIDTH = 800

	root = Tk()
	#taille fenetre
	canvas = Canvas(root, height = HEIGHT, width = WIDTH )

	canvas.pack()

	############ Menu ###################
	#menubar = Menu(interface_client)
	#menubar.add_command(label="Arbo", command=arbo)
	#interface_client.config(menu=menubar)

	############################ fond ###############################

	#background_image = PhotoImage(file='logo_6.png')
	#backgroung_label = Label(root, image=background_image)
	#backgroung_label.place(relwidth = 1 , relheight = 1)

	########################### Frame #######################################

	#Frame permet de créer des frames a l'interieur d'une fenetre
	Framefirst = Frame(root, bg = 'pink', bd = 5)
	Framefirst.place(relx = 0.5 , rely = 0.1 , relwidth= 0.75, relheight = 0.1 , anchor='n')

	#Titre et saisi de l'identifiant 
	IDlab = Label(Framefirst,text = 'Identifiant',bg='pink' ,fg = 'black')
	IDlab.place(relx = 0.048, rely = 0.1 , relwidth= 0.2, relheight = 0.4)

	IdEntry = Entry(Framefirst, text = 'ex : Paula' , fg = 'black')
	IdEntry.place(relx = 0.01, rely = 0.5 , relwidth= 0.3, relheight = 0.3)

	#Titre et saisi du mot de passe
	MDPlab = Label(Framefirst, text= 'Mot de passe', bg='pink' ,fg = 'black')
	MDPlab.place(relx = 0.4, rely = 0.1 , relwidth= 0.2, relheight = 0.4)

	MDPEntry = Entry(Framefirst)
	MDPEntry.place(relx = 0.355, rely = 0.5 , relwidth= 0.3, relheight = 0.3)

	#Bouton entrer
	Button_connexion = Button(Framefirst, text = 'Connexion', font = 20, command = auth)
	Button_connexion.place(relx = 0.69, relwidth= 0.3, relheight = 1)

	######################    Deuxieme Frame    #######################
	def frame_deux():
		"""
			la frame s'affiche seulement si l'utilisateur est connécté
		"""
		global frame_choix
		frame_choix = Frame(root, bg = 'pink', bd = 6 )
		frame_choix.place(relx = 0.5 , rely = 0.255, relwidth= 0.75, relheight = 0.7 , anchor='n')

		#Demande l'option au client 

		Option = Label(frame_choix, text = "Choisissez l'option désirée :",bg = 'pink', fg = 'black', font = 20)
		Option.place(relx = 0.3, rely = 0, relwidth = 0.4, relheight = 0.1)

		#Les différentes options 

		DownloadFill = Button(frame_choix, text = 'Download', command = download_ig)
		DownloadFill.place(relx = 0.3 , rely = 0.2, relwidth= 0.2, relheight = 0.1)

		UploadFill = Button(frame_choix, text = 'Upload', command = upload_ig)
		UploadFill.place(relx = 0.5 , rely = 0.2, relwidth= 0.2, relheight = 0.1)

		# Bouton pour deconnexion

		Button_deconnexion = Button(frame_choix, text = "Se déconnecter", font = 14, command = deconnexion_ig)
		Button_deconnexion.place(relx = 0.7 , rely = 0.9, relwidth= 0.3, relheight = 0.09)





	root.mainloop()