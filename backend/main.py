import os
import time
import subprocess
import pandas as pd

def listagem(): 
    """
    Execute o comando 'ps aux' e retorne a saída decodificada.
    """
    command = "ps aux"
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, error = process.communicate()
        return out.decode()
    except Exception as e:
        print(f"Erro ao executar 'ps aux': {e}")
        return ""

def salvar_em_csv(data, arquivo): 
    """
    Salva os dados em um arquivo CSV usando Pandas.
    """
    if not os.path.isfile(arquivo):
        data.to_csv(arquivo, index=False)
    else:
        data.to_csv(arquivo, mode='a', header=False, index=False)

def salvar_em_binario(data, arquivo): 
    """
    Salva os dados em um arquivo binário usando Pandas.
    """
    if not os.path.isfile(arquivo):
        data.to_pickle(arquivo)
    else:
        df = pd.read_pickle(arquivo)
        df = pd.concat([df, data], ignore_index=True)
        df.to_pickle(arquivo)

def rotular_processo(processo):
    """
    Rotula um único processo e retorna um dicionário com os rótulos.
    """
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

def main():
    """
    A cada 30 segundos, cria uma nova lista com os processos e salva em um arquivo CSV e um arquivo binário usando Pandas.
    """
    os.makedirs("datasets", exist_ok=True)
    arquivo_processos_csv = 'datasets/processos.csv'
    arquivo_processos_binario = 'datasets/processos.pkl'
    while True:
        output_processos = listagem().split('\n')
        dados_processos = [rotular_processo(processo) for processo in output_processos if processo]
        dados_processos = [dados for dados in dados_processos if dados is not None]  # Remover entradas None
        df = pd.DataFrame(dados_processos)
        salvar_em_csv(df, arquivo_processos_csv)
        salvar_em_binario(df, arquivo_processos_binario)
        time.sleep(5)

if __name__ == "__main__":
    main()
