# Lucas Lima Fernandes
# https://github.com/lucaslimafernandes

from collections import namedtuple

class CommandError(Exception):
    pass

class Disconnect(Exception):
    pass

Error = namedtuple("Error", ("message",))

#eof
