from enum import Enum

class Alpha(Enum):
    A0 = (0, 0)
    A1 = (2, 1)
    A2 = (4, 2)
    A3 = (8, 3)
    A4 = (3, 4)
    A5 = (6, 5)
    A6 = (12, 6)
    A7 = (11, 7)
    A8 = (5, 8)
    A9 = (10, 9)
    A10 = (7, 10)
    A11 = (14, 11)
    A12 = (15, 12)
    A13 = (13, 13)
    A14 = (9, 14)
    A15 = (1, 15)

    def __init__(self, value, power):
        self._value_ = value
        self.power = power

    def get_value(self):
        return self._value_

    def get_power(self):
        return self.power

    def __str__(self):
        return f"{self.get_value():04b} [{self.get_value()}] (A{self.power})"
    
    def __add__(self, other):
        return Alpha.get_alpha_by_value(self.get_value() ^ other.get_value())

    def __sub__(self, other):
        return Alpha.get_alpha_by_value(self.get_value() ^ other.get_value())

    def __mul__(self, other):
        power_result = (self.get_power() + other.get_power()) % 15
        power_result = 15 if power_result == 0 else power_result
        return Alpha.get_alpha_by_power(power_result)

    def __truediv__(self, other):
        other = self.inverse(other)
        return self * other
    
    @staticmethod
    def array_to_binary_string(arr):
        binary_strings = [f"{alpha.get_value():04b} [{alpha.get_value()}] (A{alpha.power})" for alpha in arr]
        return ", ".join(binary_strings)
    
    @staticmethod
    def add_arrays(arr1, arr2):
        if len(arr1) != len(arr2):
            raise ValueError("Arrays must have the same length for addition")
        
        result = []
        for alpha1, alpha2 in zip(arr1, arr2):
            result.append(alpha1 + alpha2)
        
        return result
    @classmethod
    def get_alpha_by_value(cls, value):
        for alpha in cls:
            if value == alpha.value:
                return alpha
        return cls.A0

    @classmethod
    def get_alpha_by_power(cls, power):
        for alpha in cls:
            if power == alpha.power:
                return alpha

    @classmethod
    def inverse(cls, a):
        if a == cls.A0:
            return cls.A0
        power_a = 15 - a.get_power()
        return cls.get_alpha_by_power(15 if power_a == 0 else power_a)
     
#global 

i = Alpha.get_alpha_by_value(1)
k = Alpha.get_alpha_by_value(2)


px1 = Alpha.get_alpha_by_value(10)
px2 = Alpha.get_alpha_by_value(6)


cx1 = Alpha.get_alpha_by_value(4)
cx2 = Alpha.get_alpha_by_value(6)


#byte sub

print(f"Px1: {px1}, Px2: {px2}")

#mixcolumn

cx = [cx1, cx2, cx2, cx1]

#key

key = [(i*Alpha.get_alpha_by_value(2))/Alpha.get_alpha_by_value(3), 
       (i-k)/Alpha.get_alpha_by_value(7), 
       (Alpha.get_alpha_by_value(3)*i+Alpha.get_alpha_by_value(4))/k, 
       (i-Alpha.get_alpha_by_value(7))]


print(f"Key: {Alpha.array_to_binary_string(key)}")

#Open text P

p = [(Alpha.get_alpha_by_value(5)*i)/i,
     (Alpha.get_alpha_by_value(7)*k)-Alpha.get_alpha_by_value(9),
     (Alpha.get_alpha_by_value(8)*i)+Alpha.get_alpha_by_value(14),
     (Alpha.get_alpha_by_value(6)-i)/((Alpha.get_alpha_by_value(5)*i)+k)]

print(f"P: {Alpha.array_to_binary_string(p)}")

#S(x)

def SB(alpha):
    if alpha == Alpha.A0:
        return px2
    return (px1/alpha)+px2

def SBm(alpha):
    if (alpha-px2) == Alpha.A0:
        return Alpha.A0
    return px1/(alpha-px2)

def SBa(alpha):
    return [SB(alpha[0]),SB(alpha[1])]

def SBma(alpha):
    return [SBm(alpha[0]),SBm(alpha[1])]

def SR(arr):
    return [arr[0],arr[3], arr[2], arr[1]]

def R(arr):
    return [arr[1], arr[0]]

def MX(arr,cx):
    arr1 = [cx[0]*arr[0]+cx[2]*arr[1],cx[1]*arr[0]+cx[3]*arr[1]]
    arr2 = [cx[0]*arr[2]+cx[2]*arr[3],cx[1]*arr[2]+cx[3]*arr[3]]
    return arr1 + arr2
def MXd(arr,cx):
    delta = cx[0]*cx[3] - cx[1]*cx[2]
    newcx = [cx[0]/delta,cx[1]/delta,cx[2]/delta,cx[3]/delta]
    return MX(arr, newcx)
# C consts

C2 = [Alpha.A1, Alpha.A0]
C4 = [Alpha.A3, Alpha.A0]
C6 = [Alpha.A5, Alpha.A0]

# W

    
W0 = [key[0], key[1]]
print(f"    W0: {Alpha.array_to_binary_string(W0)}")
W1 = [key[2], key[3]]
print(f"    W1: {Alpha.array_to_binary_string(W1)}")
W2 = Alpha.add_arrays(Alpha.add_arrays(W0, C2), SBa(R(W1)))
print(f"    W2: {Alpha.array_to_binary_string(W2)}")
W3 = Alpha.add_arrays(W1, W2)
print(f"    W3: {Alpha.array_to_binary_string(W3)}")
W4 = Alpha.add_arrays(Alpha.add_arrays(W2, C4), SBa(R(W3)))
print(f"    W4: {Alpha.array_to_binary_string(W4)}")
W5 = Alpha.add_arrays(W3, W4)
print(f"    W5: {Alpha.array_to_binary_string(W5)}")
W6 = Alpha.add_arrays(Alpha.add_arrays(W4, C6), SBa(R(W5)))
print(f"    W6: {Alpha.array_to_binary_string(W6)}\n")
#Encrypt
Xe = Alpha.add_arrays(p, W0+W1)
print(f"    Xe0: {Alpha.array_to_binary_string(Xe)}")
Xe = [SB(elem) for elem in Xe]
print(f"    Xe1.1: {Alpha.array_to_binary_string(Xe)}")
Xe = SR(Xe)
print(f"    Xe1.2: {Alpha.array_to_binary_string(Xe)}")
Xe = MX(Xe,cx)
print(f"    Xe1.3: {Alpha.array_to_binary_string(Xe)}")
Xe = Alpha.add_arrays(Xe, W2+W3)
print(f"    Xe1.4: {Alpha.array_to_binary_string(Xe)}")
Xe = [SB(elem) for elem in Xe]
print(f"    Xe2.1: {Alpha.array_to_binary_string(Xe)}")
Xe = SR(Xe)
print(f"    Xe2.2: {Alpha.array_to_binary_string(Xe)}")
Xe = Alpha.add_arrays(Xe, W4+W5)
print(f"    Xe2.3: {Alpha.array_to_binary_string(Xe)}")
#
print(f"Encrypt: {Alpha.array_to_binary_string(Xe)}")
#Decrypt
Xd = Alpha.add_arrays(Xe, W4+W5)
print(f"    Xd0: {Alpha.array_to_binary_string(Xd)}")
Xd = SR(Xd)
print(f"    Xd1.1: {Alpha.array_to_binary_string(Xd)}")
Xd = [SBm(elem) for elem in Xd]
print(f"    Xd1.2: {Alpha.array_to_binary_string(Xd)}")
Xd = Alpha.add_arrays(Xd, W2+W3)
print(f"    Xd1.3: {Alpha.array_to_binary_string(Xd)}")
Xd = MXd(Xd,cx)
print(f"    Xd1.4: {Alpha.array_to_binary_string(Xd)}")
Xd = SR(Xd)
print(f"    Xd2.1: {Alpha.array_to_binary_string(Xd)}")
Xd = [SBm(elem) for elem in Xd]
print(f"    Xd2.2: {Alpha.array_to_binary_string(Xd)}")
Xd = Alpha.add_arrays(Xd, W0+W1)
print(f"    Xd2.3: {Alpha.array_to_binary_string(Xd)}")
#
print(f"Decrypt: {Alpha.array_to_binary_string(Xd)}")