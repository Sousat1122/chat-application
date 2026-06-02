import socket
import threading
import json
from datetime import datetime

class ServidorChat:
    def __init__(self, host='localhost', porta=5000):
        self.host = host
        self.porta = porta
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clientes = {}  # {socket: {'nome': str, 'endereco': tuple}}
        self.lock = threading.Lock()
        
    def iniciar(self):
        """Inicia o servidor e aguarda conexões"""
        try:
            self.servidor.bind((self.host, self.porta))
            self.servidor.listen(5)
            print(f"[SERVIDOR] Iniciado em {self.host}:{self.porta}")
            print(f"[SERVIDOR] Aguardando conexões de clientes...")
            
            while True:
                cliente_socket, endereco = self.servidor.accept()
                print(f"[NOVA CONEXÃO] {endereco}")
                
                # Inicia thread para gerenciar o cliente
                thread_cliente = threading.Thread(
                    target=self.gerenciar_cliente,
                    args=(cliente_socket, endereco)
                )
                thread_cliente.daemon = True
                thread_cliente.start()
                
        except Exception as e:
            print(f"[ERRO] {e}")
        finally:
            self.servidor.close()
    
    def gerenciar_cliente(self, cliente_socket, endereco):
        """Gerencia um cliente individual"""
        nome_cliente = None
        
        try:
            # Recebe o nome do cliente
            dados = cliente_socket.recv(1024).decode('utf-8')
            mensagem = json.loads(dados)
            
            if mensagem.get('tipo') == 'conexao':
                nome_cliente = mensagem.get('nome', f'Utilizador_{endereco[1]}')
                
                with self.lock:
                    self.clientes[cliente_socket] = {
                        'nome': nome_cliente,
                        'endereco': endereco
                    }
                
                # Notifica todos os clientes da nova conexão
                self.broadcast({
                    'tipo': 'sistema',
                    'mensagem': f'{nome_cliente} entrou no chat',
                    'timestamp': datetime.now().strftime('%H:%M:%S'),
                    'utilizadores': self.obter_utilizadores()
                })
                
                print(f"[CLIENTE CONECTADO] {nome_cliente} ({endereco})")
            
            # Loop para receber mensagens
            while True:
                dados = cliente_socket.recv(1024).decode('utf-8')
                
                if not dados:
                    break
                
                try:
                    mensagem = json.loads(dados)
                    
                    if mensagem.get('tipo') == 'mensagem':
                        # Prepara a mensagem para broadcast
                        mensagem_formatada = {
                            'tipo': 'mensagem',
                            'remetente': nome_cliente,
                            'conteudo': mensagem.get('conteudo', ''),
                            'timestamp': datetime.now().strftime('%H:%M:%S')
                        }
                        
                        print(f"[MENSAGEM] {nome_cliente}: {mensagem.get('conteudo')}")
                        self.broadcast(mensagem_formatada)
                        
                except json.JSONDecodeError:
                    print(f"[ERRO] Formato inválido recebido de {endereco}")
                    
        except Exception as e:
            print(f"[ERRO] Conexão com {endereco}: {e}")
        
        finally:
            # Remove o cliente
            with self.lock:
                if cliente_socket in self.clientes:
                    nome = self.clientes[cliente_socket]['nome']
                    del self.clientes[cliente_socket]
                    
                    # Notifica saída
                    self.broadcast({
                        'tipo': 'sistema',
                        'mensagem': f'{nome} saiu do chat',
                        'timestamp': datetime.now().strftime('%H:%M:%S'),
                        'utilizadores': self.obter_utilizadores()
                    })
                    
                    print(f"[CLIENTE DESCONECTADO] {nome}")
            
            cliente_socket.close()
    
    def broadcast(self, mensagem):
        """Envia mensagem para todos os clientes conectados"""
        with self.lock:
            for cliente_socket in self.clientes.keys():
                try:
                    dados = json.dumps(mensagem, ensure_ascii=False)
                    cliente_socket.sendall(dados.encode('utf-8'))
                except Exception as e:
                    print(f"[ERRO] Ao enviar broadcast: {e}")
    
    def obter_utilizadores(self):
        """Retorna lista de utilizadores conectados"""
        return [info['nome'] for info in self.clientes.values()]


if __name__ == '__main__':
    servidor = ServidorChat(host='0.0.0.0', porta=5000)
    servidor.iniciar()