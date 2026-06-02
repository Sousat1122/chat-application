import socket
import threading
import json
import sys
from datetime import datetime

class ClienteChat:
    def __init__(self, host='localhost', porta=5000):
        self.host = host
        self.porta = porta
        self.socket = None
        self.conectado = False
        self.nome = None
        
    def conectar(self, nome_utilizador):
        """Conecta ao servidor de chat"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.porta))
            self.conectado = True
            self.nome = nome_utilizador
            
            # Envia mensagem de conexão
            mensagem_conexao = json.dumps({
                'tipo': 'conexao',
                'nome': self.nome
            }, ensure_ascii=False)
            self.socket.sendall(mensagem_conexao.encode('utf-8'))
            
            print(f"✓ Conectado ao servidor em {self.host}:{self.porta}")
            print(f"✓ Bem-vindo, {self.nome}!")
            print("\n--- Digite 'sair' para desconectar ---\n")
            
            # Inicia thread para receber mensagens
            thread_recepcao = threading.Thread(target=self.receber_mensagens)
            thread_recepcao.daemon = True
            thread_recepcao.start()
            
            # Loop principal para envio de mensagens
            self.loop_envio()
            
        except ConnectionRefusedError:
            print(f"✗ Erro: Não foi possível conectar ao servidor em {self.host}:{self.porta}")
            print("  Certifique-se que o servidor está a correr!")
        except Exception as e:
            print(f"✗ Erro de conexão: {e}")
        finally:
            self.desconectar()
    
    def loop_envio(self):
        """Loop principal para envio de mensagens"""
        while self.conectado:
            try:
                mensagem = input()
                
                if mensagem.lower() == 'sair':
                    break
                
                if mensagem.strip():  # Ignora mensagens vazias
                    dados = json.dumps({
                        'tipo': 'mensagem',
                        'conteudo': mensagem
                    }, ensure_ascii=False)
                    self.socket.sendall(dados.encode('utf-8'))
                    
            except KeyboardInterrupt:
                print("\n")
                break
            except Exception as e:
                print(f"✗ Erro ao enviar: {e}")
                break
    
    def receber_mensagens(self):
        """Thread para receber mensagens do servidor"""
        while self.conectado:
            try:
                dados = self.socket.recv(1024).decode('utf-8')
                
                if not dados:
                    break
                
                try:
                    mensagem = json.loads(dados)
                    self.processar_mensagem(mensagem)
                except json.JSONDecodeError:
                    print(f"✗ Erro ao descodificar mensagem")
                    
            except Exception as e:
                if self.conectado:
                    print(f"✗ Erro na receção: {e}")
                break
    
    def processar_mensagem(self, mensagem):
        """Processa e exibe as mensagens recebidas"""
        tipo = mensagem.get('tipo')
        
        if tipo == 'mensagem':
            remetente = mensagem.get('remetente')
            conteudo = mensagem.get('conteudo')
            timestamp = mensagem.get('timestamp')
            
            print(f"\n[{timestamp}] {remetente}: {conteudo}")
            print("> ", end="", flush=True)
            
        elif tipo == 'sistema':
            conteudo = mensagem.get('mensagem')
            timestamp = mensagem.get('timestamp')
            utilizadores = mensagem.get('utilizadores', [])
            
            print(f"\n[{timestamp}] SISTEMA: {conteudo}")
            if utilizadores:
                print(f"  Utilizadores online: {', '.join(utilizadores)}")
            print("> ", end="", flush=True)
    
    def desconectar(self):
        """Desconecta do servidor"""
        self.conectado = False
        if self.socket:
            self.socket.close()
        print("\n✓ Desconectado do servidor")


if __name__ == '__main__':
    print("="*50)
    print("  CLIENTE DE CHAT - SISTEMA DISTRIBUÍDO")
    print("="*50)
    
    # Configurações
    host = input("Endereço do servidor [localhost]: ").strip() or 'localhost'
    porta_str = input("Porta do servidor [5000]: ").strip() or '5000'
    
    try:
        porta = int(porta_str)
    except ValueError:
        print("✗ Porta inválida")
        sys.exit(1)
    
    nome_utilizador = input("Seu nome de utilizador: ").strip()
    
    if not nome_utilizador:
        print("✗ Nome de utilizador não pode estar vazio")
        sys.exit(1)
    
    cliente = ClienteChat(host, porta)
    cliente.conectar(nome_utilizador)