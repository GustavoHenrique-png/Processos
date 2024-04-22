import os
import time
import subprocess
import pandas as pd
import pickle

def listagem(): 
    command = "ps aux"
    proccess = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, erro = proccess.communicate()
    return out.decode()

def arquivo(data, processos): # escreve os processos listados em um arquivo
    with open(processos, "ab") as file:
        pickle.dump(data, file)

def rotulaProcesso(processos):
    dados = processos.split()
    if dados[0] == 'USER':
        return None
    return {
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

def main(): # a cada 30s cria uma nova lista com os processos
    contador = 1
    os.makedirs("datasets", exist_ok=True)  
    arquivoProcessos = 'datasets/processos.pkl'
    while True:
        processos = listagem().split('\n') #dividindo a saída em linhas
        dadosProcessos = [rotulaProcesso(processo) for processo in processos if processo]
        dadosProcessos = [dados for dados in dadosProcessos if dados is not None]
        arquivo(dadosProcessos, arquivoProcessos)
        time.sleep(30)  # adicionando um intervalo de 30 segundos

if __name__ == "__main__":
    main()
