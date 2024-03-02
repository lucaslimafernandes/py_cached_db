# Lucas Lima Fernandes
# https://github.com/lucaslimafernandes

# from protocol import ProtocolHandler
import socket
import pickle
from json import dumps, loads

class Disconnect(Exception):
    pass


class Client:
    def __init__(self, host="localhost", port=31333):
        self.host = host
        self.port = port

        self.client_socket = None
        self.connected = False
    
        self.__connect()
    
    def __connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))

            self.connected = True
        except Disconnect as e:
            print(f"Erro: {e.__class__.__name__} - {e}")
    
    def disconnect(self):
        if self.client_socket:
            self.client_socket.close()
        self.connected = False

    def execute(self, command, *args):
        message = command + " " + " ".join(args)
        self.client_socket.send(message.encode())
        response = self.client_socket.recv(4096)
        return pickle.loads(response)

    def get(self, key):
        _res = loads(self.execute("GET", key))
        return _res

    def get_all(self, schema="default") -> dict:
        # _res = loads(self.execute("AGET", schema))
        return self.execute("AGET", schema)

    def get_keys(self, schema="default") -> list:
        return self.execute("KGET", schema)

    def set(self, key, value, schema="default"):
        value = dumps(value)
        return self.execute("SET", key, value, schema)

    def delete(self, key, schema="default"):
        return self.execute("DELETE", key, schema)

    def flush(self):
        return self.execute("FLUSH")

    def close(self):
        self.client_socket.close()

    def __del__(self):
        self.close()



if __name__ == "__main__":
    cliente = Client()
    print(cliente.set("nova_chave", "novo_valor"))
    print(cliente.get("nova_chave"))
    print(cliente.delete("nova_chave"))
    print(cliente.flush())
    print(cliente.get_all())
    cliente.close()
