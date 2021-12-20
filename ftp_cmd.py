#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# ftp.py
# FTP CLI interface
#
# Copyright (C) 2007 Pierre "delroth" Bourdon <delroth@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

# http://sdz.tdct.org/sdz/utiliser-le-module-ftp-de-python.html
#     se connecter à un serveur FTP ;
#     envoyer un fichier sur le serveur ;
#     créer un dossier ;
#     renommer un fichier ou un dossier ;
#     supprimer un fichier ou un dossier ;
#     changer le répertoire courant ;
#     lister tous les fichiers et dossiers d'un répertoire ;
#     envoyer une commande au serveur (sans passer par des fonctions Python) ;
#     change répertoire

#     recevoir les messages renvoyés par le serveur après chaque action.

import ftplib as ftp # on importe le module et on la renomme juste pour le script en "ftp"
 
commands = {} # on crée le dictionnaire qui contiendra toutes les commandes &amp; descriptions
ghost = ''
guser = ''

def connection(value=None):
    if value == None:
        return getattr(connection, 'value', None)
    else:
        connection.value = value
        return value

# fonction decorator pour ajouter la fonction qui l'appelle au dictionnaire commands 
def ftpcommand(nom_court, description): 
    def decorator(function):
        #print(nom_court,':',description)
        global commands # on n'oublie pas de mettre le dico commands global, sinon ça va en redéfinir un
        commands[nom_court] = (function, description) # on ajoute au dictionnaire
        return function
    return decorator

# ici on appelle le décorateur : il va s'occuper d'ajouter la fonction help avec sa description au dictionnaire commands
@ftpcommand("help", "Affiche l'aide des commandes") 
def help(): # définition de la commande, juste après @ftpcommand car ON EST OBLIGÉS
    global commands
    keys = commands.keys() # on récupère les clés == fonctions dans notre cas    
    # on trie par ordre alphabétique :)  #keys_list.sort() erreur!!
    for n,i in enumerate(sorted(keys)):
        print(n+1,i+" : "+commands[i][1]) # on affiche le nom de la fonction et sa description
 
@ftpcommand("connect", "Se connecte au serveur. Syntaxe: connect <host> <user> <password>")
def connect(host, user, password):
    global ghost, guser
    ghost = host
    guser = user
    try:
        state = connection(ftp.FTP(host, user, password))
        #print(state)
        print(state.getwelcome())        
    except ftp.all_errors as e:
        print('Erreur de connexion ', ghost, guser)
        print("%s" % e)
    return state.getwelcome()    
 
@ftpcommand("ls", "Liste le contenu du répertoire actuel")
def ls():
    try:
        # on affiche le listing du répertoire
        connection().dir()  # renvoi None
    except AttributeError:
        print("Erreur : vous n'êtes pas connecté !")
 
@ftpcommand("deco", "Se déconnecte du serveur. Syntaxe: deco")
def deco():
    try:
        connection().quit() # la déconnexion avec quit()
        print('Déconnexion de', ghost, guser)
    except:
        print('Erreur Déconnexion')
        
@ftpcommand("envoi", "Envoie un fichier au serveur. Syntaxe: envoi <adresse_fichier>")
def envoi(adresse_fichier):
    try:
        fichier = adresse_fichier
        file = open(fichier, 'rb') # on ouvre le fichier en mode "read-binary"
        connection().storbinary('STOR '+fichier, file) # envoi
        file.close() # fermeture du fichier
        print('Upload successful')
    except:
        print('Erreur Upload')     
        
@ftpcommand("rename", "Renomme un fichier. Syntaxe: rename <avant> <apres>")
def rename(avant, apres):
    try:
        renommer, renommer_en = avant, apres
        rename = connection().rename(renommer, renommer_en) # on renomme
        print(rename)
    except:
        print('Erreur Rename')
        
@ftpcommand("changedir", "Change de répertoire. Syntaxe: changedir <dir>")
def changedir(dir):
    change = connection().cwd(dir) # on change de répertoire
    print(change)
    
@ftpcommand("efface", "Efface un fichier. Syntaxe : efface <fichier>")
def efface(fichier):
        effacer = fichier
        delete = connection().delete(effacer) # on efface
 
@ftpcommand("creer_rep", "Crée un répertoire (dossier). Syntaxe : creer_rep <nom>")
def creer_rep(nom):
        rep = nom
        repertoire = connection().mkd(rep) # on crée le répertoire
 
@ftpcommand("sup_rep", "Supprimer un répertoire (dossier). Syntaxe : sup_rep <nom>")
def sup_rep(nom):
        supprimer = nom
        delete_dir = connection().rmd(supprimer) # on supprime le répertoire
 
@ftpcommand("cmd", "Envoie une commande au serveur. Syntaxe: cmd <commande>")
def cmd(commande):
        resultat = connection().sendcmd(commande) # on envoi la commande

@ftpcommand("upload", "Envoie de fichiers vers le serveur. Syntaxe: upload <host> <user> <pwd")
def upload(host, user, pwd):
    ret = connect(host, user, pwd)
    if '220' in ret:
        # distant working directory
        changedir('streaming/html')
        try:
            efface('index.html')
        except:
            pass

        envoi('index.html')
        deco()
    else:
        print('Pas de connexion')
 
# un petit message à propos de la license du script :)
welcome = '''ftp.py version 1.0, Copyright (C) 2007
 
ftp.py comes with ABSOLUTELY NO WARRANTY. This is free software, and you are
welcome to redistribute it under certain conditions; see the GNU General Public
License for more details: http://www.gnu.org/licenses/old-licenses/gpl-2.0.html'''
 
def main():
    global commands
    print(welcome) # affichage du message ci-dessus
    help()
    def command_to_argv(cmd):
        #print(cmd)
        argv = cmd.split(' ') # on met dans une liste les différents arguments
        argv_size = len(argv) # on compte le nombre de paramètres
        #print(argv)
        i = 0 # on initialise le compteur
        while i < argv_size:
            if argv[i].endswith('\\') and i + 1 != argv_size: # si c'est un nom de fichier du type : test\ 1.py
                argv[i] = argv[i][:-1] + " " + argv[i + 1] # on ajoute le "1.py" à "test", ce qui fait "test 1.py"
                del argv[i + 1]
                argv_size -= 1
            i += 1 # on incrémente le compteur
        return argv # on retourne les arguments
    while True: # boucle infinie, il va encore falloir utiliser break pour en sortir
        try: cmd = command_to_argv(input('> ')) # si la commande entrée provoque une erreur...
        except EOFError: return 0 # on quitte la boucle
        except KeyboardInterrupt: return 0 # on quitte la boucle
 
        cmdname, args = cmd[0], cmd[1:] # cmdname = fonction appelée, args = arguments
        if not cmdname in commands.keys(): # si la fonction appelée n'existe pas dans le script
            print("Erreur: '%s' commande incorrecte." % cmdname) # on affiche un message d'erreur
            continue
        try:
            commands[cmdname][0](*args)
        except TypeError:
            print("Erreur: mauvais nombre d'arguments pour '%s' command." % cmdname)
        except AttributeError:
            print("Erreur : vous n'êtes pas connecté !")
    return 0
 
import sys
if __name__ == "__main__":
    #main()
    sys.exit(main()) # si le script est utilisé comme un module, on n'exécute pas le script