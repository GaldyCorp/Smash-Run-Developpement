from pickle import GLOBAL
from zipfile import ZipFile
import os
from tkinter import filedialog
import shutil
import requests
import sys


def instal(dir=""):
    while dir=="":
        dir=filedialog.askdirectory(mustexist=True)
        print(dir)
    try:
        os.mkdir(dir+"/sm-run")
    except:
        shutil.rmtree(dir+"/sm-run")
        os.mkdir(dir+"/sm-run")
       
    #shutil.copyfile("main.py", dir+"/sm-run/setup.py")
    os.chdir(dir+"/sm-run")
    ver=input("Quelle version voulez vous installer ? ")
    link = "https://github.com/GaldyCorp/Smash-Run/archive/refs/heads/sm-run_v"+str(ver)+".zip"
    file_name = "sm-run_v"+str(ver)+".zip"
    retry=0
    while True:
        with open(file_name, "wb") as f:
            print("Téléchargement %s" % file_name)
            try:
                response = requests.get(link, stream=True, allow_redirects=True)
                total_length = response.headers.get('content-length')
            except:
                print("Connection impossible, vérifiez votre connexion.")
                while True:
                    try:
                        response = requests.get(link, stream=True, allow_redirects=True)
                        break
                    except:
                        None
                continue
            if total_length is None: # no content length header
                f.write(response.content)
                print("Reconnection au serveur...")
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s] %s / %s" % ('=' * done, ' ' * (50-done),dl,total_length) )    
                    sys.stdout.flush()
                if dl==total_length:
                    if total_length==14:
                        print("\nVersion innexistante ou url non valide.")
                        return 101
                    else:
                        break
                else:
                    print("Erreur lors du telechargement.\nNouvelle tentative en cours... ("+str(retry)+")")
                    retry+=1
    print("\nExtraction...")
    with ZipFile(file_name, 'r') as zip:
        zip.extractall()
    os.rename("Smash-Run-"+file_name[:-4],"bin")
    os.remove(file_name)
    print("Installation Fini")
    return 0


instal()
input()