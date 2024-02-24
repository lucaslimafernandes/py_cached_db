# Lucas Lima Fernandes
# https://github.com/lucaslimafernandes

import socket
import pickle

from errors import CommandError, Disconnect, Error


# class ProtocolHandler(object):
#     def handle_request(self, socket_file):
#         pass

#     def write_response(self, socket_file, data):
#         pass


class Server(object):
    
    def __init__(
        self,
        host='127.0.0.1',
        port=31334
        ) -> None:
        
        self.host = host
        self.port = port

        self._kv = {
            "default": {}
        }

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self._commands:dict = self.get_commands()

    def start(self):

        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)

        print('Aguardando conexão...')
        conn, addr = self.server_socket.accept()
        print('Conectado a:', addr)
        self.connection_handler(conn)


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
            # "MGET": self.mget,
            # "MSET": self.mset,
        }

    def get(self, key:str, schema="default"):
        _tmp_kv:dict = self._kv[schema]
        return _tmp_kv.get(key)

    def set(self, key:str, value, schema="default"):        
        self._kv[schema][key] = value
        return True

    def delete(self, key, schema="default"):
        _tmp_kv:dict = self._kv[schema]
        if key in _tmp_kv:
            del self._kv[key]
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
        self._kv = {
            "default": {}
        }
        return kvlen

    # TODO:
    # def mget(self, *keys):
    #     return [self._kv.get(key) for key in keys]

    # def mset(self, *items):
    #     data = zip(items[::2], items[1::2])
    #     for key, value in data:
    #         self._kv[key] = value
    #     return len(data)

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



#eof
