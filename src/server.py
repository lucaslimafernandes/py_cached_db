# Lucas Lima Fernandes
# https://github.com/lucaslimafernandes

import socket
import pickle
import threading

from errors import CommandError, Disconnect, Error


class Server(object):
    def __init__(self, host="127.0.0.1", port=31334) -> None:
        self.host = host
        self.port = port

        # Mudança de esquema não está funcionando
        self._kv = {"default": {}}

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self._commands: dict = self.get_commands()

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)

        print("Aguardando conexões...")
        while True:
            conn, addr = self.server_socket.accept()
            print('Conectado a:', addr)

            # Iniciar uma nova thread para lidar com a conexão
            client_thread = threading.Thread(target=self.connection_handler, args=(conn,))
            client_thread.start()
        # conn, addr = self.server_socket.accept()
        # print("Conectado a:", addr)
        # self.connection_handler(conn)

    def connection_handler(self, conn):
        while True:
            try:
                data = conn.recv(4096)
                if not data:
                    raise CommandError("Empty data.")

                mensagem = data.decode()
                # Processa a mensagem
                comando, *args = mensagem.split()
                if comando in self._commands:
                    response = self._commands[comando](*args)
                else:
                    response = "Comando não reconhecido."

                conn.send(pickle.dumps(response))

            except Disconnect:
                break
        conn.close()

    def get_commands(self) -> dict:
        return {
            "GET": self.get,
            "SET": self.set,
            "DELETE": self.delete,
            "FLUSH": self.flush,
            "AGET": self.aget,
            "KGET": self.kget,
        }

    def get(self, key: str, schema="default"):
        _tmp_kv: dict = self._kv[schema]
        return _tmp_kv.get(key)

    def aget(self, schema="default"):
        return self._kv[schema]

    def kget(self, schema="default"):
        return [i for i in self._kv[schema].keys()]

    def set(self, key: str, value, schema="default"):
        self._kv[schema][key] = value
        return True

    def delete(self, key, schema="default"):
        _tmp_kv: dict = self._kv[schema]
        if key in _tmp_kv:
            del self._kv[schema][key]
            return True
        return False

    def delete_schema(self, schema):
        if schema in self._kv:
            del self._kv[schema]
            return True
        return False

    def flush(self):
        kvlen = len(self._kv)
        self._kv.clear()
        self._kv = {"default": {}}
        return kvlen

    def get_response(self, data):
        if not isinstance(data, list):
            try:
                data = data.split()
            except:
                raise CommandError("Request must be list or simple string.")

        if not data:
            raise CommandError("Missing command.")

        command = data[0].upper()
        if command not in self._commands:
            raise CommandError(f"Unrecognized command: {command}")

        return self._commands[command](*data[1:])


# eof
