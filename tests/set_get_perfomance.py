from client import Client
from time import time




def n_inserts(number=1000) -> dict:

    t0 = time()
    pc = Client()
    for n in range(0, number):
        pc.set(str(n), n)
    
    return {f'n_inserts_{number}': time() - t0}


def n_gets(number=1000) -> dict:

    t0 = time()
    pc = Client()
    for n in range(0, number):
        pc.get(str(n))
    
    return {f'n_gets_{number}': time() - t0}



if __name__ == '__main__':

    ins = n_inserts()
    gets = n_gets()

    print(ins)
    print(gets)

