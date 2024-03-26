import subprocess
import time

def listar_processos():
    comando = "ps aux"
    processo = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    saida, erro = processo.communicate()
    return saida.decode()

def criar_arquivo(lista_processos, nome_arquivo):
    with open(nome_arquivo, "w") as arquivo:
        arquivo.write(lista_processos)

def main():
    contador = 1
    while True:
        lista_processos = listar_processos()
        nome_arquivo = f"lista_de_processos_{contador}.txt"
        criar_arquivo(lista_processos, nome_arquivo)
        print(f"Arquivo {nome_arquivo} atualizado.")
        contador += 1
        time.sleep(30)

if __name__ == "__main__":
    main()
