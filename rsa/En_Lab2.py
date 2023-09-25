def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    phi0, x0, x1 = phi, 0, 1
    while e > 1:
        q = e // phi
        phi, e = e % phi, phi
        x0, x1 = x1 - q * x0, x0
    return x1 + phi0 if x1 < 0 else x1

def find_factors(n):
    p = 2
    while p * p <= n:
        if n % p == 0:
            q = n // p
            return p, q
        p += 1
    return None, None

# n and e - open key, c - encrypt text
n = 1073
e = 13
c = 342

# n = 667
# e = 17
# c = 219

#print n, e, c
print(f"n:{n}, e:{e}, c:{c}")

# find p and q
p, q = find_factors(n)
print(f"p:{p}, q:{q}")

#check p and q
if p == None or q == None:
        print(" Error in p and q")
        
#find phi
phi = (p - 1) * (q - 1)
print(f"phi: {phi}")

#check e
if gcd(e, phi) != 1:
        print("Error in E")
        
#find d
d = mod_inverse(e, phi)
print(f"d: {d}")

#decrypt text
m = pow(c, d, n)
print(f"m: {m}")

#encrypt back
c = pow(m, e, n)
print(f"c: {c}")

#Create sign
sign = pow(m, d, n)
print(f"sign: {sign}")

#Test sign

sign_test = pow(sign, e, n)
print(f"sign_test: {sign_test}")