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
GF = 19

n2 = 192
e2 = 13

n1 = 1073
e1 = 13
c1 = 342

a = 3

#print n, e, c
print(f"n2: {n2}, e2: {e2}")

# find p and q
p2, q2 = find_factors(n2)
print(f"p2: {p2}, q2: {q2}")

#check p and q
if p2 == None or q2 == None:
        print(" Error in p2 and q2")
        
#find phi
phi2 = (p2 - 1) * (q2 - 1)
print(f"phi2: {phi2}")

#check e
if gcd(e2, phi2) != 1:
        print("Error in E2")
        
#find d
d2 = mod_inverse(e2, phi2)
print(f"d2: {d2}")

#print n, e, c
print(f"n1: {n1}, e1: {e1}, c1: {c1}")

# find p and q
p1, q1 = find_factors(n1)
print(f"p1: {p1}, q1: {q1}")

#check p and q
if p1 == None or q1 == None:
        print(" Error in p1 and q1")
        
#find phi
phi1 = (p1 - 1) * (q1 - 1)
print(f"phi1: {phi1}")

#check e
if gcd(e1, phi1) != 1:
        print("Error in E1")
        
#find d
d1 = mod_inverse(e1, phi1)
print(f"d1: {d1}")

#decrypt text
m = pow(c1, d1, n1)
print(f"m: {m}")

x1 = d1
x2 = d2

print(f"x1: {x1}, x2: {x2}")

y1 = pow(a, d1, GF)
y2 =  pow(a, d2, GF)

print(f"y1: {y1}, y2: {y2}")

y12 = pow(y2, d1, GF)
y21 =  pow(y1, d2, GF)

print(f"y12: {y12}, y21: {y21}")

erm = pow(m, d1, n1)

print(f"Er(m): {erm}")

print(f"Message: ({m}, {erm})")