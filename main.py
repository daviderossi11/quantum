from qiskit import QuantumCircuit, QuantumRegister, transpile
from qiskit.circuit.library import HGate, RYGate, XGate
from numpy import arcsin, sqrt, pi
import math
from matplotlib import pyplot as plt

# Funzione per calcolare il valore di θ
def calculate_theta(value, max_value):
    X_N = value / sqrt(max_value)
    return 2 * arcsin(X_N)

# definisco dei memory values
memory_values = [4, 5, 10, 3, 7, 4, 5, 12]

N = len(memory_values)
n = int(math.log2(N))

max_value = sum([x**2 for x in memory_values])
thetas = [calculate_theta(value, max_value) for value in memory_values]

qaddr = QuantumRegister(n, 'addr')
qdata = QuantumRegister(1, 'data')

circuit = QuantumCircuit(qaddr, qdata)

for qa in qaddr:
    circuit.append(HGate(), [qa])
circuit.barrier()



for i, el in enumerate(memory_values):
    theta = calculate_theta(el, max_value)
    binary_index = bin(i)[2:].zfill(n)
    
    for j, bit in enumerate(binary_index):
        if bit == '0':
            circuit.append(XGate(), [qaddr[j]])
    
    CRYGate = RYGate(theta).control(n)
    circuit.append(CRYGate, qaddr[:n] + [qdata[0]])
    
    for j, bit in enumerate(binary_index):
        if bit == '0':
            circuit.append(XGate(), [qaddr[j]])
    
    circuit.barrier()


optimized_circuit = transpile(circuit, optimization_level=2)
print(optimized_circuit)

print(f"Depth: {optimized_circuit.depth()} - Size: {optimized_circuit.size()}\n")
print(circuit)

print(f"Depth: {circuit.depth()} - Size: {circuit.size()}\n")