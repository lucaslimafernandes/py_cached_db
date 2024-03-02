# py_cached_db

A Pure Python in-memory key-value store.

by Lucas Lima Fernandes

## Use

### Install

Only Linux XD

run shell file install_service.sh

```sudo bash install_service.sh```

### List of commands

#### SET

Stores a key-value pair in the key-value store under a specified schema.

#### GET

Retrieves the value associated with a given key from the key-value store under a specified schema.

#### DELETE

Removes a key-value pair from the key-value store under a specified schema, if the key exists.

#### FLUSH

Clears all key-value pairs stored in the key-value store.

#### AGET

Retrieves the entire key-value store under a specified schema.

#### KGET

Retrieves a list of keys stored in the key-value store under a specified schema.

### Use

Clone file src/client.py

```
from client import Client
c = Client()

print(c.set("nova_chave", "novo_valor"))
print(c.get("nova_chave"))
print(c.delete("nova_chave"))
print(c.flush())
print(c.get_all())
c.close()

```
