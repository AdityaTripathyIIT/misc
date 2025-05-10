import socket

server_ip = "192.168.0.107"
server_port = 24 

server = socket.socket(socket.AF_INET, socket.SOCk_STREAM)

server.listen(1)

client_sock, client_addr = server.accept()

data_recv = client_socket.rev(4096)
printf(data_recv.decode())

client_sock.send(b"That's what she said!")
client_sock.close()
