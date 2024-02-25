# Lucas Lima Fernandes
# https://github.com/lucaslimafernandes

# from protocol import ProtocolHandler
import socket
import pickle

from errors import Disconnect, CommandError, Error


class Client:
    def __init__(self, host="localhost", port=31333):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    def execute(self, command, *args):
        message = command + " " + " ".join(args)
        self.client_socket.send(message.encode())
        response = self.client_socket.recv(4096)
        return pickle.loads(response)

    def get(self, key):
        return self.execute("GET", key)

    def get_all(self, schema="default"):
        return self.execute("AGET", schema)

    def get_keys(self, schema="default"):
        return self.execute("KGET", schema)

    def set(self, key, value, schema="default"):
        value = self._types(value)
        return self.execute("SET", key, value, schema)

    def delete(self, key, schema="default"):
        return self.execute("DELETE", key, schema)

    def flush(self):
        return self.execute("FLUSH")

    def close(self):
        self.client_socket.close()

    def __del__(self):
        self.close()

    def _types(self, a):
        if isinstance(a, int):
            return f"int({str(a)})"
        else:
            return a


if __name__ == "__main__":
    cliente = Client()
    print(cliente.get("chave1"))
    print(cliente.set("nova_chave", "novo_valor"))
    print(cliente.get("nova_chave"))
    print(cliente.delete("nova_chave"))
    print(cliente.get("nova_chave"))
    print(cliente.flush())
    print(cliente.get("chave2"))
    cliente.close()
