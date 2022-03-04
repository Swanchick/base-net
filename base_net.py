from collections import Callable
import uuid
import socket
import threading
import json

class Server:
    def __init__(self, address: str = "localhost", port: int = 50000, listen: int = 10):
        self.address = address
        self.port = port
        self.listen = listen
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.work = True
        self.clients = {}
    
    def is_valid(self, message: str) -> bool:
        try:
            json.loads(message)
        except:
            return False

        return True

    def get_info(self, client: socket.socket) -> tuple:
        return self.clients[client]

    def get_uuid(self, client: socket.socket) -> str:
        return self.get_info(client)[0]
    
    def get_addr_info(self, client: socket.socket) -> tuple:
        return self.get_info(client)[1]

    def get_connected(self) -> str:
        return f"Client: {len(list(self.clients.keys()))}/{self.listen}"

    def on_receive(self, client, data: str):
        pass

    def on_connected(self, client: socket.socket, info: tuple):
        key = uuid.uuid4().hex
        
        client.send(key.encode())

        listening_client = threading.Thread(target=self.listen_client, args=(client,))
        listening_client.start()

        self.clients[client] = (key, info)

        print(self.get_connected())
    
    def connect_client(self):
        while self.work:
            client, info = self.sock.accept()

            self.on_connected(client, info)

    def listen_client(self, client: socket.socket):
        while self.work:
            data = client.recv(1024)
            message = data.decode()

            if self.is_valid(message):
                self.on_receive(client, message)
            else:
                print("Client is disconnected")
                client.close()
                self.clients.pop(client)
                print(self.get_connected())
                return

    def send_all(self, message: str):
        for client in list(self.clients.keys()):
            data = {"message": message, "key": self.get_uuid(client)}
            _json = json.dumps(data)
            client.send(_json.encode())

    def start(self):
        self.sock.bind((self.address, self.port))
        self.sock.listen(self.listen)

        print("Server was started...")

        self.connect_client()

class Client:
    def __init__(self, address: str = "localhost", port: int = 50000):
        self.address = address
        self.port = port
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.work = True
    
    def disconnect(self):
        self.work = False
        self.sock.close()

    def on_receive_data(self, data: str):
        pass

    def receive_server(self):
        while self.work:
            data = self.sock.recv(1024)
            self.on_receive_data(data)
    
    def on_connected(self):
        data = self.sock.recv(1024)
        self.key = data.decode()

    def send_data(self, data: str):
        _json = {"message": data, "key": self.key}
        
        message = str(json.dumps(_json))

        self.sock.send(message.encode())

    def start(self):
        print("Client was started...")
        self.sock.connect((self.address, self.port))
        self.on_connected()

        thread_receive = threading.Thread(target=self.receive_server)
        thread_receive.start()
            