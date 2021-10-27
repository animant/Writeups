import socket
import re


def V(deg, p, t):
    if deg == 0: return 2
    elif deg == 1: return t
    else:
         return V(1,p,t)*V(deg-1,p,t)-p*V(deg-2,p,t)
    


def ext(k,p,deg):
    t = p+1-k
    return p**deg+1 -V(deg,p,t)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("168.119.108.148", 13010))
for i in range(10000):
    tmpstr = s.recvfrom(4024)[0]
    print(tmpstr)
    try:
        p = int(re.findall(r'p = [0-9]+', tmpstr)[0][4:])
        k = int(re.findall(r'k = [0-9]+', tmpstr)[0][4:])
        n = int(re.findall(r'n = [0-9]+', tmpstr)[0][4:])
        order = ext(k,p,n)
        print("order = ", order)
        s.send(str(order)+"\r\n")
    except:
        pass
        

s.close()
