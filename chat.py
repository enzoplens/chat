from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

#Conexão
uri = "mongodb+srv://enzoplensalmeida:dito1910@consultas.li8yd.mongodb.net/?retryWrites=true&w=majority&appName=Consultas"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.chat
collection = db.teste

#Função para gerar uma chave com base em uma senha
def generate_key(password):
    key = sum([ord(c) for c in password]) % 256
    return key

#Função para cifrar a mensagem
def encrypt(message, key):
    encrypted_message = ''.join(chr((ord(c) + key) % 256) for c in message)
    return encrypted_message

#Função para decifrar a mensagem
def decrypt(encrypted_message, key):
    decrypted_message = ''.join(chr((ord(c) - key) % 256) for c in encrypted_message)
    return decrypted_message

# Função para inserir mensagem no banco de dados (evita duplicatas)
def insert_message(sender, recipient, message, password):
    key = generate_key(password)
    encrypted_message = encrypt(message, key)
    # Verifica se a mensagem já foi inserida
    if not collection.find_one({'sender': sender, 'recipient': recipient, 'message': encrypted_message}):
        collection.insert_one({
            'sender': sender,
            'recipient': recipient,
            'message': encrypted_message,
        })

# Função para buscar e decifrar mensagens no banco de dados
def get_messages(recipient, password):
    user_messages = []
    key = generate_key(password)
    for msg in collection.find({'recipient': recipient}):
        decrypted_message = decrypt(msg['message'], key)
        user_messages.append((msg['sender'], decrypted_message))
    return user_messages

#Loop para envio e recebimento de mensagens
while True:
    
    recipient = input("Escolha o destinatário: ")
    password = input("senha para esta conversa: ")
    
    #Mostra mensagens antigas
    mensagens_antigas = get_messages(recipient, password)
    if mensagens_antigas:
        print(f"Mensagens anteriores para {recipient}:")
        for sender, message in mensagens_antigas:
            print(f"De: {sender}, Mensagem: {message}")
    else:
        print(f"Nenhuma mensagem antiga para {recipient}.")

    #Envio de mensagem
    user_message = input(f"Você para {recipient}: ")
    insert_message("Você", recipient, user_message, password)

    #Exibir mensagens recebidas
    mensagens_recebidas = get_messages(recipient, password)
    print(f"Mensagens recebidas de {recipient}:")
    for sender, message in mensagens_recebidas:
        print(f"De: {sender}, Mensagem: {message}")