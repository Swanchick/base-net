import base_net
import json

ADDRESS = "localhost"
PORT = 50000
LISTEN = 10

class ServerUi(base_net.Server):
    def __init__(self, *args):
        super().__init__(*args)
    
    def on_receive(self, client, data):
        print(data)
        _json = json.loads(data)
        self.send_all(_json["message"])
        

if __name__ == "__main__":
    server = ServerUi(ADDRESS, PORT, LISTEN)
    server.start()