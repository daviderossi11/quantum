from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import RYGate, XGate, HGate
from qiskit.transpiler import PassManager, preset_passmanagers
from qiskit.providers.fake_provider import GenericBackendV2
from numpy import arcsin, sqrt, pi
import math
from matplotlib import pyplot as plt

# Funzione per calcolare il valore di θ
def calculate_theta(value, max_value):
    X_N = value / sqrt(max_value)
    return 2 * arcsin(X_N)

# Valori iniziali e calcolo di θ
memory_values = [3, 2, 1, 3]
max_value = sum([x**2 for x in memory_values])
thetas = [calculate_theta(value, max_value) for value in memory_values]
N = len(memory_values)
n = int(math.log2(N))

# Registri quantistici
qaddr = QuantumRegister(n, 'addr')
qdata = QuantumRegister(1, 'data')

circuit = QuantumCircuit(qaddr, qdata)

# Inizializzazione degli indirizzi
for qa in qaddr:
    circuit.append(HGate(), [qa])
circuit.barrier()

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

backend= GenericBackendV2(3)
# Configurazione del backend e ottimizzazione
pass_manager = preset_passmanagers.generate_preset_pass_manager(
    optimization_level=2,
    backend=backend
)

# Traspilazione del circuito
optimized_circuit = pass_manager.run(circuit)


# Visualizzazione del circuito

print(optimized_circuit)



