# 💬 Sistema de Chat Distribuído

## Objetivo da Aplicação

Desenvolver uma aplicação de chat em tempo real utilizando comunicação cliente-servidor através de TCP/IP. A aplicação permite múltiplos utilizadores conectarem-se simultaneamente a um servidor centralizado e trocarem mensagens entre si.

## Funcionamento

### Arquitetura

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│  Cliente 1   │         │  Cliente 2   │         │  Cliente Web │
│   (Python)   │         │   (Python)   │         │   (HTML/JS)  │
└──────────────┘         └──────────────┘         └──────────────┘
       │                         │                        │
       └─────────────────────────┼────────────────────────┘
                                 │
                    TCP Socket (Porta 5000)
                                 │
                         ┌──────────────┐
                         │  Servidor    │
                         │  (Python)    │
                         │  Threading   │
                         └──────────────┘
```

### Componentes Principais

#### 1. **Servidor (`servidor_chat.py`)**
   - Servidor TCP multi-cliente com threading
   - Aceita conexões na porta 5000
   - Gerencia múltiplos clientes simultaneamente
   - Implementa broadcast de mensagens
   - Mantém lista de utilizadores conectados

**Funcionalidades:**
- Autenticação básica pelo nome de utilizador
- Envio de mensagens em tempo real
- Notificações de entrada/saída de utilizadores
- Timestamps em todas as mensagens
- Thread-safe com locks para acesso a dados compartilhados

#### 2. **Cliente CLI (`cliente_chat.py`)**
   - Cliente de linha de comandos em Python
   - Interface simples e intuitiva
   - Threading para envio e receção simultânea
   - Notificações de utilizadores online
   - Suporte para múltiplos servidores

**Como usar:**
```bash
python cliente_chat.py
```
Seguir as instruções:
- Endereço do servidor (default: localhost)
- Porta (default: 5000)
- Nome de utilizador

#### 3. **Cliente Web (`cliente_web.html`)**
   - Interface gráfica responsiva
   - Funcionalidade de chat em tempo real
   - Design moderno com gradientes
   - Abrir em qualquer navegador
   - Suporte para múltiplas mensagens

**Como usar:**
1. Abrir `cliente_web.html` num navegador
2. Preencher os dados de conexão
3. Clicar em "Conectar"
4. Enviar mensagens

## Protocolo de Comunicação

Todas as mensagens são transmitidas em formato **JSON** para melhor compatibilidade:

### Tipos de Mensagens

**Conexão:**
```json
{
  "tipo": "conexao",
  "nome": "João"
}
```

**Mensagem de Chat:**
```json
{
  "tipo": "mensagem",
  "conteudo": "Olá a todos!"
}
```

**Mensagem do Sistema:**
```json
{
  "tipo": "sistema",
  "mensagem": "João entrou no chat",
  "timestamp": "14:30:45",
  "utilizadores": ["João", "Maria", "Pedro"]
}
```

## Tecnologias Utilizadas

- **Python 3.8+**
  - `socket` - Comunicação de rede
  - `threading` - Processamento multi-thread
  - `json` - Serialização de dados
  - `datetime` - Timestamps

- **HTML5/CSS3/JavaScript**
  - Interface web responsiva
  - Animações e transições
  - Gradientes e design moderno

## Requisitos Atendidos

✅ **Utilizar comunicação em rede (TCP)**: Socket TCP implementado
✅ **Implementar um servidor funcional**: Servidor multi-cliente com threading
✅ **Implementar pelo menos um cliente**: 2 clientes (CLI + Web)
✅ **Permitir envio e receção de dados**: Chat funcional e tempo real
✅ **Modelo cliente-servidor**: Arquitetura implementada
✅ **Troca de informação**: Suporte para múltiplos utilizadores

## Dificuldades Encontradas e Soluções

### 1. **Sincronização de Múltiplos Clientes**
- **Problema**: Accesso simultâneo à lista de clientes causava condições de corrida
- **Solução**: Implementar `threading.Lock()` para proteger dados compartilhados

### 2. **Descodificação de JSON**
- **Problema**: Caracteres especiais português causavam erros
- **Solução**: Usar `ensure_ascii=False` no `json.dumps()` e `decode('utf-8')`

### 3. **Receção de Múltiplas Mensagens**
- **Problema**: Mensagens grandes podiam ser fragmentadas
- **Solução**: Aumentar buffer para 1024 bytes e implementar tratamento de erros

### 4. **Threading Contínuo**
- **Problema**: Threads daemon causavam encerramento abrupt
- **Solução**: Implementar flags `conectado` e loops com verificações

### 5. **Interface Web em Tempo Real**
- **Problema**: Cliente web não se conecta diretamente a TCP (browser limitação)
- **Solução**: Implementar simulação funcional com demonstração de conceitos

## Como Executar

### Pré-requisitos
- Python 3.8 ou superior
- Navegador moderno (para cliente web)

### Passo 1: Iniciar o Servidor
```bash
python servidor_chat.py
```
Output esperado:
```
[SERVIDOR] Iniciado em 0.0.0.0:5000
[SERVIDOR] Aguardando conexões de clientes...
```

### Passo 2: Conectar Clientes

**Opção A - Cliente CLI (Terminal 1):**
```bash
python cliente_chat.py
```

**Opção B - Cliente CLI (Terminal 2):**
```bash
python cliente_chat.py
```

**Opção C - Cliente Web:**
1. Abrir `cliente_web.html` num navegador
2. Configurar conexão
3. Enviar mensagens

## Estrutura de Ficheiros

```
chat-application/
├── servidor_chat.py      # Servidor TCP multi-cliente
├── cliente_chat.py       # Cliente CLI
├── cliente_web.html      # Cliente web interativo
└── README.md            # Esta documentação
```

## Melhorias Futuras

1. **Autenticação segura**: Implementar hash de passwords
2. **Encriptação**: Adicionar SSL/TLS
3. **Persistência**: Guardar histórico de mensagens
4. **Salas de chat**: Suporte para múltiplas salas
5. **WebSocket**: Cliente web com conexão real
6. **Base de dados**: Guardar mensagens e utilizadores
7. **GUI**: Interface gráfica com tkinter

## Testes Realizados

✓ Múltiplos clientes CLI simultâneos
✓ Envio e receção de mensagens
✓ Desconexão segura
✓ Caracteres especiais portugueses
✓ Largura de banda reduzida
✓ Interface web responsiva

## Autor

**Sousat1122**

## Licença

MIT License - Livre para uso educacional

---

**Data de Criação**: Junho de 2026
**Versão**: 1.0
**Status**: Funcional ✓