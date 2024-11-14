from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import HGate, CXGate, RYGate, XGate
from numpy import arcsin, sqrt, pi
import math
from matplotlib import pyplot as plt
# Funzione per calcolare il valore di θ
def calculate_theta(value, max_value):
    X_N = value / sqrt(max_value)
    return 2 * arcsin(X_N)

# Funzione per calcolare la profondità e la dimensione del circuito per diverse dimensioni del dataset
def calculate_circuit_metrics(memory_values):
    max_value = sum([x**2 for x in memory_values])
    thetas = [calculate_theta(value, max_value) for value in memory_values]
    N = len(memory_values)
    n = int(math.log2(N))
    
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


    return circuit.depth(), circuit.size()

# Generare dataset di diverse dimensioni (potenze di 2)
dataset_sizes = [2**i for i in range(1, 10)]
depths = []
sizes = []

for size in dataset_sizes:
    memory_values = list(range(1, size + 1))
    depth, size = calculate_circuit_metrics(memory_values)
    depths.append(depth)
    sizes.append(size)


# Disegnare i grafici
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(dataset_sizes, depths, marker='o')
plt.xlabel('Dataset Size')
plt.ylabel('Circuit Depth')
plt.title('Circuit Depth vs Dataset Size')

plt.subplot(1, 2, 2)
plt.plot(dataset_sizes, sizes, marker='o')
plt.xlabel('Dataset Size')
plt.ylabel('Circuit Size')
plt.title('Circuit Size vs Dataset Size')

plt.tight_layout()
plt.show()

"""TO DO : 
    XGate nel circuito
    plot circuit depth all'aumentare della dim del vector(power 2)
    plot circuit size // ore 11 merc 30/10
    Formula annulamento XGate su bit uguali
    
    Ricorda
    Gate universali set diversi
    Grafico sulla size/depth
    transpile

    Greycode
    Standard
    Cratività

    rappresentazione qubit ottimizzazione xgate

    transpiler.optimization_level

    plot grafici size e depth su dataset e al variare dell'oottimization level

    
"""
