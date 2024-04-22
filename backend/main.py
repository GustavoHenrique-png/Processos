import os
import time
import subprocess
import pandas as pd
import pickle

def listagem(): #inserido o comando no shell, aqui do linux
    command = "ps aux"
    proccess = subprocess.Popen(command, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, erro = proccess.communicate()
    return out.decode()

def arquivo(data, processos):#escreve os processos listado em um arquivo
    with open(processos,"ab") as file:
        pickle.dump(data, file)

def rotulaProcesso(processos):
    dados = processos.split
    return{
        'USER': dados[0],
        'PID': int(dados[1]),
        '%CPU': float(dados[2]),
        '%MEM': float(dados[3]),
        'VSZ': int(dados[4]),
        'RSS': int(dados[5]),
        'TTY': dados[6],
        'STAT': dados[7],
        'START': dados[8],
        'TIME': dados[9],
        'COMMAND': ' '.join(dados[10:])
    }

def main():#a cada 30s cria uma nova lista com os processos
    contador = 1
    os.makedirs("datasets")
    arquivoProcessos = 'datasets/processos.pkl'
    while True:
        processos = listagem()
        dadosProcessos = [rotulaProcesso(processo) for processo in processos if processo]
        arquivo(dadosProcessos,arquivoProcessos)

if __name__ =="__main__":
    main()

#rotular dados
#definir um dataset para criar um treinamento robusto sem muitos falsos resultados
#buscar outros S.O
#tipos de ameaças
#achar uma ameça controlavel
