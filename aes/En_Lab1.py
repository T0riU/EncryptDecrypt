class Alpha:
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return f"{self.value:04b} [{self.value}]"

    def __add__(self, other):
        return Alpha(self.value ^ other.value)

    def __sub__(self, other):
        return Alpha(self.value ^ other.value)

    def __mul__(self, other):
        result = 0
        temp = self.value
        temp1 = other.value
        if self.value == 0:
            temp1 = self.value
            temp = other.value
        for _ in range(4):
            if  temp1 & 1:
                result ^= temp
            high_bit_set = temp & 0x08
            temp <<= 1
            if high_bit_set:
                temp ^= 0x13  
            temp1 >>= 1
        return Alpha(result)
    
    def __truediv__(self, other):
        if other.value == 0:
           return self

        inverse = None
        for i in range(16):
            if (other * Alpha(i)).value == 1:
                inverse = Alpha(i)
                break
        
        if inverse is None:
            return self
        if  self.value == 0:
            return inverse

        return self * inverse
    @staticmethod
    def array_to_binary_string(arr):
        binary_strings = [f"{alpha.value:04b} [{alpha.value}]" for alpha in arr]
        return ", ".join(binary_strings)
    @staticmethod
    def add_arrays(arr1, arr2):
        if len(arr1) != len(arr2):
            raise ValueError("Arrays must have the same length for addition")
        
        result = []
        for alpha1, alpha2 in zip(arr1, arr2):
            result.append(alpha1 + alpha2)
        
        return result
    
i = Alpha(1)
k = Alpha(2)

px1 = Alpha(10)
px2 = Alpha(6)

cx1 = Alpha(4)
cx2 = Alpha(6)


#byte sub
print(f"\ni: {i}, k: {k}")
print(f"Px1: {px1}, Px2: {px2}")


#mixcolumn

cx = [cx1, cx2, cx2, cx1]

#key

key = [(i*Alpha(2))/Alpha(3), 
       (i-k)/Alpha(7), 
       (Alpha(3)*i+Alpha(4))/k, 
       (i-Alpha(7))]


print(f"Key: {Alpha.array_to_binary_string(key)}")

#Open text P

p = [(Alpha(5)*i)/i,
     (Alpha(7)*k)-Alpha(9),
     (Alpha(8)*i)+Alpha(14),
     (Alpha(6)-i)/((Alpha(5)*i)+k)]

print(f"P: {Alpha.array_to_binary_string(p)}")


def SB(alpha):
    if alpha.value == 0:
        return px2
    return (px1/alpha)+px2

def SBm(alpha):
    if (alpha-px2).value == 0:
        return Alpha(0)
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
    arr1 = [cx[0]*arr[0]+arr[1]*cx[2],
            cx[1]*arr[0]+
            arr[1]*cx[3]]
    arr2 = [cx[0]*arr[2]+cx[2]*arr[3],
            cx[1]*arr[2]+cx[3]*arr[3]]
    return arr1 + arr2
def MXd(arr,cx):
    delta = cx[0]*cx[3] - cx[1]*cx[2]
    newcx = [cx[0]/delta,cx[1]/delta,cx[2]/delta,cx[3]/delta]
    return MX(arr, newcx)
# C consts

C2 = [Alpha(2), Alpha(0)]
C4 = [Alpha(8), Alpha(0)]
C6 = [Alpha(6), Alpha(0)]

# W

    
W0 = [key[0], key[1]]
print(f"    W0: {Alpha.array_to_binary_string(W0)}")
W1 = [key[2], key[3]]
print(f"    W1: {Alpha.array_to_binary_string(W1)}")
# print(f"C2: {Alpha.array_to_binary_string(C2)}")
# print(f"SBa(R(W1)): {Alpha.array_to_binary_string(SBa(R(W1)))}")
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
print(f"P:{Alpha.array_to_binary_string(p)}")
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
print(f"    Xd1.3: {Alpha.array_to_binary_string(Xd)}")# 4 0 5 14
Xd = MXd(Xd,cx)
print(f"    Xd1.4: {Alpha.array_to_binary_string(Xd)}")#0 7 15 5 \\ 14 13 15 5
Xd = SR(Xd)
print(f"    Xd2.1: {Alpha.array_to_binary_string(Xd)}")
Xd = [SBm(elem) for elem in Xd]
print(f"    Xd2.2: {Alpha.array_to_binary_string(Xd)}")
Xd = Alpha.add_arrays(Xd, W0+W1)
print(f"    Xd2.3: {Alpha.array_to_binary_string(Xd)}")
#
print(f"Decrypt: {Alpha.array_to_binary_string(Xd)}")