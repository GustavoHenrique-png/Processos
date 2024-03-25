import os
import time
import subprocess

def listagem():#inserido o comando no shell, aqui do linux

    command = 'ps aux'
    proccess = proccess.POpen(command, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, erro = proccess.comunicate
    return out.decode()

def arquivo(listaProcessos, arquivoProcessos): #escreve os processos listado em um arquivo
    with open(arquivoProcessos,"w") as archive:
        archive.write(listaProcessos)
    

def main():#a cada 30s cria uma nova lista com os processos
    contador = 1

    while True:
        listaProcessos = listagem()
        arquivoProcessos = f"listinhaDeProcessos_{contador}.txt"
        arquivo(listaProcessos,arquivoProcessos)
        contador += 1
        time.sleep(30)



if __name__ =="__main__":
    main()