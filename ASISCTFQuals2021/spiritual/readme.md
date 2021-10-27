Spiritual
==========
The meaning of spirituality has developed and expanded over time, but what does it mean here?

```nc 168.119.108.148 13010```

Solution
=========
The order of elliptic curve is: ```#E(F_p) = p-1 + t```.

For extended fields: ```math #E(F_p^k) = p-1 + V_k```, where ```V_k``` is defined recursively: ```V_0 = 1, V_1 = t, V_n = V_1xV_{n-1} - px V_{n-2}```
Thus, when we know an order ```#E(F_p)``` and prime ```p``` it's easy to compute *t* and ```#E(F_p^k)```. All you need is to do it automaticaly until you get a flag.

