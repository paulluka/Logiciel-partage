import os

fichier = input('Fichier a copier : ')
#
with open(fichier, "rb") as f:
	data = f.read()
	f.close()
	
fich = input("nv fichier : ")

with open(fich, "wb") as v:
	v.write(data)
	v.close
	os.system("pause")

os.system('pause')
