import os
import time
import subprocess
import pandas as pd

def listagem(): #inserindo o comando no terminal e buscando a saida codificada
    command = "ps aux"
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, error = process.communicate()
        return out.decode()
    except Exception as e:#tratando erro caso o camando não funcione 
        print(f"Erro ao executar 'ps aux': {e}")
        return ""

def salvaCSV(data, arquivo): #Usando o pandas para salvar o arquvivo em csv pra facilitar a leitura 
    if not os.path.isfile(arquivo):#Verificando a existência do arquivo
        data.to_csv(arquivo, index=False)#Criando o arquivo caso ele não exista
    else:
        data.to_csv(arquivo, mode='a', header=False, index=False)#posicionando o cursor no fim do arquivo ja criado a cada interação

def salvaBinario(data, arquivo): 
    if not os.path.isfile(arquivo):#Verificando exitencia do arquivo binario
        data.to_pickle(arquivo)#criando caso não exista
    else:#posicionando o cursor no fim do arquivo ja criando a cada interação
        df = pd.read_pickle(arquivo)
        df = pd.concat([df, data], ignore_index=True)
        df.to_pickle(arquivo)

def rotulaProcesso(processo):#Separando e rotulando as colunas do data set pra retornar um dicionario
    dados = processo.split()
    if dados[0] == 'USER':  # Ignora o cabeçalho
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

def main():#Laço que cria os arquivos a cada determinado tempo
    os.makedirs("datasets", exist_ok=True)#criando a pasta do dataset
    arquivo_processos_csv = 'datasets/processos.csv'#setando arquivo binario
    arquivo_processos_binario = 'datasets/processos.pkl'#setando arquivo csv
    while True:#Laço da criação
        output_processos = listagem().split('\n')#separando a listagem em linhas
        dados_processos = [rotulaProcesso(processo) for processo in output_processos if processo] #verificação das entradas obtidas
        dados_processos = [dados for dados in dados_processos if dados is not None]  # Remover entradas None
        df = pd.DataFrame(dados_processos) #criação do dataframe
        salvaCSV(df, arquivo_processos_csv)#salvando o dataframe em csv
        salvaBinario(df, arquivo_processos_binario)#salvando em binario
        time.sleep(5)#tempo de rodar dnv

if __name__ == "__main__":
    main()
