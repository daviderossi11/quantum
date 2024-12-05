from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import RYGate, XGate, HGate
from qiskit.transpiler import PassManager, preset_passmanagers
from qiskit.providers.fake_provider import GenericBackendV2
from numpy import arcsin, sqrt, pi
import math
from matplotlib import pyplot as plt

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

# Funzione per calcolare il valore di θ
def calculate_theta(value, max_value):
    X_N = value / sqrt(max_value)
    return 2 * arcsin(X_N)

# Valori iniziali e calcolo di θ
memory_values = range(2**)
max_value = sum([x**2 for x in memory_values])
thetas = [calculate_theta(value, max_value) for value in memory_values]
N = len(memory_values)
n = int(math.log2(N))

# Registri quantistici
qaddr = QuantumRegister(n, 'addr')
qcaddr = QuantumRegister(n, 'caddr')
previous_bit = [1] * n
qdata = QuantumRegister(1, 'data')
qcdata = QuantumRegister(1, 'cdata')


circuit = QuantumCircuit(qaddr, qdata)
qc= QuantumCircuit(qcaddr, qcdata)

# Inizializzazione degli indirizzi
for qa in qaddr:
    circuit.append(HGate(), [qa])
circuit.barrier()

for qa in qcaddr:
    qc.append(HGate(), [qa])
circuit.barrier()


gray_codes = gray_code(n)

binary_index = list(enumerate(gray_codes[0]))
for i, el in enumerate(memory_values):
    theta = calculate_theta(el, max_value)
    for j, bit in binary_index:
        if bit == '0' and previous_bit[j] == 1:
            qc.append(XGate(), [qaddr[j]])
        
        previous_bit[j] = int(bit)
        
    
    CRYGate = RYGate(theta).control(n)
    qc.append(CRYGate, qaddr[:n] + [qdata[0]])
    

    if i < N - 1:
        binary_index = list(enumerate(gray_codes[i + 1]))
        for j, next_bit in binary_index:
            if next_bit == '1' and previous_bit[j] == 0:
                qc.append(XGate(), [qaddr[j]])
    else:
        for j,  bit in binary_index:
            if bit == '0':
                qc.append(XGate(), [qaddr[j]])


    qc.barrier()

# Applicazione dei controlli e dei CRY gate
for i, el in enumerate(memory_values):
    theta = calculate_theta(el, max_value)
    binary_index = bin(i)[2:].zfill(n)

    # Applicazione delle NOT per configurare l'indirizzo
    for j, bit in enumerate(binary_index):
        if bit == '0':
            circuit.append(XGate(), [qaddr[j]])

    # Applicazione del CRY controllato
    CRYGate = RYGate(theta).control(n)
    circuit.append(CRYGate, qaddr[:n] + [qdata[0]])

    # Ripristino delle NOT
    for j, bit in enumerate(binary_index):
        if bit == '0':
            circuit.append(XGate(), [qaddr[j]])

    circuit.barrier()

backend= GenericBackendV2(n+1)
circutit_size= []
qc_size = []
# Configurazione del backend e ottimizzazione
for i in range(0, 4):
    pass_manager = preset_passmanagers.generate_preset_pass_manager(
    optimization_level=i,
    backend=backend
    )

    optimized_circuit = pass_manager.run(circuit)
    optimized_qc = pass_manager.run(qc)
    circutit_size.append(optimized_circuit.size())
    qc_size.append(optimized_qc.size())

# Plotting





