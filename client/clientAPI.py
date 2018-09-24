import socket


host = "127.0.0.1"
port = 25565

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((host, port))
client.send(b"Hello World!!")

response = client.recv(4096)

print(response)
