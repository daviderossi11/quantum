from math import log2
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.transpiler import preset_passmanagers
from qiskit.providers.fake_provider import GenericBackendV2
from qiskit.circuit.library import HGate, RYGate, XGate
from numpy import arcsin, sqrt


# Funzione per calcolare il gray code
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


# Funzione per calcolare la profondità e la dimensione del circuito per diverse dimensioni del dataset
def ffqram_metrics_classic(N, memory_values=None,barrier=True,opt_lvl=2):
    if memory_values is None:
        memory_values = list(range(1, N + 1))
    
    max_value = sum([x**2 for x in memory_values])
    thetas = [calculate_theta(value, max_value) for value in memory_values]
    n = int(log2(N))
    
    qaddr = QuantumRegister(n, 'addr')
    qdata = QuantumRegister(1, 'data')
    circuit = QuantumCircuit(qaddr, qdata)
    
    for qa in qaddr:
        circuit.append(HGate(), [qa])
    if barrier:
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

        if barrier:
            circuit.barrier()

    pass_manager = preset_passmanagers.generate_preset_pass_manager(
        optimization_level=opt_lvl,
        backend=GenericBackendV2(n+1)
    )

    optimized_circuit = pass_manager.run(circuit)


    
    
    return circuit.depth(), optimized_circuit.depth(), circuit.size(), optimized_circuit.size()



def ffqram_metrics_graycode(N, memory_values=None,barrier=True,opt_lvl=2):
    if memory_values is None:
        memory_values = list(range(1, N + 1))
    
    max_value = sum([x**2 for x in memory_values])
    thetas = [calculate_theta(value, max_value) for value in memory_values]
    n = int(log2(N))
    
    qaddr = QuantumRegister(n, 'addr') 
    qdata = QuantumRegister(1, 'data')
    previous_bit = [1] * n

    circuit = QuantumCircuit(qaddr, qdata)

    for qa in qaddr:
        circuit.append(HGate(), [qa])
    if barrier:
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
        if barrier:
            circuit.barrier()

    pass_manager = preset_passmanagers.generate_preset_pass_manager(
        optimization_level=opt_lvl,
        backend=GenericBackendV2(n+1)
    )

    optimized_circuit = pass_manager.run(circuit)

    return circuit.depth(), optimized_circuit.depth(), circuit.size(), optimized_circuit.size()     
