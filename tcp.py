import socket

target_host = "www.google.com"
target_port = 80
'''
AF_INET -> address family = IPv4 (for IPv6 -> AF_INET6)
SOCK_STREAM -> using TCP protocol (other ,common - but not TOO common -, protocol to use is UDP)
'''

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#The followig syntax is - i believe - special to TCP. It takes a (1, 2) array with target host(string or IPvX address) and a port
client.connect((target_host, target_port))

client.send(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

response = client.recv(4096)

print(response.decode)
client.close()
