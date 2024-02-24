from gevent.pool import Pool
from gevent.server import StreamServer

from errors import CommandError, Disconnect, Error


class ProtocolHandler(object):
    def handle_request(self, socket_file):
        pass

    def write_response(self, socket_file, data):
        pass


class Server(object):
    
    def __init__(
        self,
        host='127.0.0.1',
        port='31333',
        max_clients=64
    ) -> None:
        
        self._pool = Pool(max_clients)
        self._server = StreamServer(
            listener=(host, port),
            handle=self.connection_handler,
            spawn=self._pool
        )

        self._protocol = ProtocolHandler()
        self._kv = {
            "default": {}
        }
        self._commands = self.get_commands()

    def connection_handler(self, conn, address):
        socket_file = conn.makefile("rwb")

        while True:
            try:
                data = self._protocol.handle_request(socket_file)

            except Disconnect:
                break

            try:
                resp = self.get_response(data)

            except CommandError as e:
                resp = Error(e.args[0])

            self._protocol.write_response(socket_file, resp)

    def get_commands(self) -> dict:
        return {
            "GET": self.get,
            "SET": self.set,
            "DELETE": self.delete,
            "FLUSH": self.flush,
            "MGET": self.mget,
            "MSET": self.mset,
        }

    def get(self, key:str, schema="default"):
        _tmp_kv:dict = self.kv[schema]
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

    def run(self):
        self._server.serve_forever()