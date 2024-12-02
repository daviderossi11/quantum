from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import HGate, CXGate, RYGate, XGate
from numpy import arcsin, sqrt, pi
import math
from matplotlib import pyplot as plt

def calculate_theta(value, max_value):
    X_N = value / sqrt(max_value)
    return 2 * arcsin(X_N)


# Funzione per generare il codice Gray
def gray_code(n):
    """Generate n-bit Gray code iteratively."""
    if n == 0:
        return ['0']
    if n == 1:
        return ['0', '1']
    
    gray_codes = ['0', '1']
    for i in range(2, n + 1):
        # Create the next sequence by reflecting the current sequence
        reflected = ['1' + code for code in reversed(gray_codes)]
        gray_codes = ['0' + code for code in gray_codes] + reflected
    
    return gray_codes

# numero di qubit
memory_values = [i for i in range(2**3)]
N = len(memory_values)
n  = int(math.log2(N))

max_value = sum([x**2 for x in memory_values])

qaddr = QuantumRegister(n, 'addr')
previous_bit = [1] * n
qdata = QuantumRegister(1, 'data')
circuit = QuantumCircuit(qaddr, qdata)
    
for qa in qaddr:
    circuit.append(HGate(), [qa])
circuit.barrier()
    
gray_codes = gray_code(n)
binary_index = list(enumerate(gray_codes[0]))
    
for i, el in enumerate(memory_values):

    theta = calculate_theta(el, max_value)

    for j, bit in binary_index:
        if bit == '0' and previous_bit[j] == 1:
            circuit.append(XGate(), [qaddr[j]])
        previous_bit[j] = int(bit)
    

    CRYGate = RYGate(theta).control(n)
    circuit.append(CRYGate, qaddr[:n] + [qdata[0]])
        
    if i < N - 1:
        binary_index = list(enumerate(gray_codes[i + 1]))
        for j, next_bit in binary_index:
            if next_bit == '1' and previous_bit[j] == 0:
                circuit.append(XGate(), [qaddr[j]])
    else:
        for j, bit in binary_index:
            if bit == '0':
                circuit.append(XGate(), [qaddr[j]])
        
    circuit.barrier()


circuit.draw('mpl', fold=30, scale=0.9)

