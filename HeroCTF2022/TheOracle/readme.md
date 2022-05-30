The oracle's apprentice
==========
Looks like Tiresias, the blind oracle, took a nice long holiday and his apprentice had to cover for him. She's new to the job so if she forgets anything... you'll just have to deal with it.

Good luck !

Host : crypto.heroctf.fr Port : 9000

Solution
=========

The oracle script is:

```python
#!/usr/bin/env python3
from Crypto.Util.number import getStrongPrime, bytes_to_long
import random

FLAG = open('flag.txt','rb').read()

encrypt = lambda m: pow(m, e, n)
decrypt = lambda c: pow(c, d, n)

e = random.randrange(3, 65537, 2)
p = getStrongPrime(1024, e=e)
q = getStrongPrime(1024, e=e)

n = p * q
φ = (p-1) * (q-1)

d = pow(e, -1, φ)

c = encrypt(bytes_to_long(FLAG))

#print(f"{n=}")
#print(f"{e=}")
print(f"{c = }")

for _ in range(3):
     t = int(input("c = "))
     print(decrypt(t)) if c != t else None
```

Here we see, the oracle first returns encrypted flag and suggests to decrypt any payload except the given encrypted flag. The idea of solution is that we use RSA homomorphism of multiplication operation to perform some kind of blinding.

Attack steps:

1. Receive encrypted flag: ```c = F^e mod n```, where F is a long int representation of flag.
2. Blind encrypted message: ```c' = c**2```.
3. Send ```c'``` to oracle for decryption. The decryption result is ```F' = c'^d mod n = (F^2e)^d mod n = F^2 mod n```
4. In this case, the flag bitsize is much shorter than RSA module. Moreover, it shorter than ```n/2```. That's why we can recover the flag F just calculating square root: ```F = nth_root(F', 2)```. The complete script:
```python
from Crypto.Util.number import long_to_bytes

def nth_root(x, n):
    # Start with some reasonable bounds around the nth root.
    upper_bound = 1
    while upper_bound ** n <= x:
        upper_bound *= 2
    lower_bound = upper_bound // 2
    # Keep searching for a better result as long as the bounds make sense.
    while lower_bound < upper_bound:
        mid = (lower_bound + upper_bound) // 2
        mid_nth = mid ** n
        if lower_bound < mid and mid_nth < x:
            lower_bound = mid
        elif upper_bound > mid and mid_nth > x:
            upper_bound = mid
        else:
            # Found perfect nth root.
            return mid
    return mid + 1

FF = input() # input blinded decrypted message
F = nth_root(FF,2)
print(long_to_bytes(F))
```
