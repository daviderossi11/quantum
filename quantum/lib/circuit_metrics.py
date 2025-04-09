from math import log2
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.transpiler import preset_passmanagers
from qiskit.providers.fake_provider import GenericBackendV2
from qiskit.circuit.library import HGate, RYGate, XGate
from numpy import arcsin, sqrt


# Funzione per calcolare il gray code
def gray_code(n):
    """
    Generate n-bit Gray code iteratively.
    Gray code is a binary numeral system where two successive values differ in only one bit.
    Parameters:
    n (int): The number of bits in the Gray code.
    Returns:
    list of str: A list containing the n-bit Gray code sequence.
    Examples:
    >>> gray_code(2)
    ['00', '01', '11', '10']
    >>> gray_code(3)
    ['000', '001', '011', '010', '110', '111', '101', '100']
    """
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
    """
    Calculate the theta angle for a given value and maximum value.

    This function computes the theta angle using the formula:
    theta = 2 * arcsin(value / sqrt(max_value))

    Args:
        value (float): The value for which to calculate the theta angle.
        max_value (float): The maximum value used for normalization.

    Returns:
        float: The calculated theta angle in radians.
    """
    X_N = value / sqrt(max_value)
    return 2 * arcsin(X_N)


# Funzione per calcolare la profondità e la dimensione del circuito per diverse dimensioni del dataset
def ffqram_metrics_classic(n, memory_values=None, barrier=True, opt_lvl=2):
    """
    Generate a quantum circuit for FFQRAM metrics and optimize it.
    This function creates a quantum circuit that encodes classical data into a quantum state
    using a specific FFQRAM (Fully Flexible Quantum RAM) encoding scheme. The circuit is then
    optimized using a preset pass manager.
    Args:
        n (int): The number of qubits in the address register.
        memory_values (list, optional): A list of classical memory values to encode. If None,
            the function will use a default list of values from 1 to N. Defaults to None.
        barrier (bool, optional): Whether to add barriers between different stages of the circuit.
            Defaults to True.
        opt_lvl (int, optional): The optimization level for the pass manager. Defaults to 2.
    Returns:
        tuple: A tuple containing the following metrics:
            - int: The depth of the original circuit.
            - int: The depth of the optimized circuit.
            - int: The size (number of gates) of the original circuit.
            - int: The size (number of gates) of the optimized circuit.
    """

    N = 2**n

    if memory_values is None:
        memory_values = list(range(1, N + 1))
    
    max_value = sum([x**2 for x in memory_values])
    
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
    
    return circuit.depth(), optimized_circuit.depth(), circuit.size(), optimized_circuit.size(), circuit.count_ops(), optimized_circuit.count_ops()



def ffqram_metrics_graycode(n, memory_values=None, barrier=True, opt_lvl=2):
    """
    Generate a quantum circuit using the FFQRAM (Fully Flexible Quantum Random Access Memory) 
    approach with Gray code addressing and calculate its metrics.
    Args:
        n (int): The number of qubits in the address register.
        memory_values (list, optional): A list of memory values to be encoded. Defaults to None, 
                                        which will generate a list of values from 1 to N.
        barrier (bool, optional): Whether to add barriers in the circuit for visualization. Defaults to True.
        opt_lvl (int, optional): The optimization level for the pass manager. Defaults to 2.
    Returns:
        tuple: A tuple containing:
            - int: Depth of the original circuit.
            - int: Depth of the optimized circuit.
            - int: Size of the original circuit.
            - int: Size of the optimized circuit.
    """

    N = 2**n
    if memory_values is None:
        memory_values = list(range(1, N + 1))
    
    max_value = sum([x**2 for x in memory_values])
    
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

    return circuit.depth(), optimized_circuit.depth(), circuit.size(), optimized_circuit.size(), circuit.count_ops(), optimized_circuit.count_ops()



def create_ffqram_gc_circuit(n,memory_values=None,opt_lvl=2,normalize=True):
    """
    Create a quantum circuit using the FFQRAM (Flip Flop Quantum Random Access Memory) approach
    with Gray code addressing.
    Args:
        n (int): The number of qubits in the address register.
        memory_values (list, optional): A list of memory values to be encoded. Defaults to None, 
                                        which will generate a list of values from 1 to N.
        opt_level (int, optional): The optimization level for the pass manager. Defaults to 2.
    Returns:
        QuantumCircuit: The quantum circuit implementing the FFQRAM encoding with Gray code addressing.
    """

    N = 2**n
    if memory_values is None:
        memory_values = list(range(1, N + 1))
    max_value = sum([x**2 for x in memory_values])
    
    qaddr = QuantumRegister(n, 'addr')
    qdata = QuantumRegister(1, 'data')
    previous_bit = [1] * n

    circuit = QuantumCircuit(qaddr, qdata)

    for qa in qaddr:
        circuit.append(HGate(), [qa])

    gray_codes = gray_code(n)
    binary_index = list(enumerate(gray_codes[0]))
    
    for i, el in enumerate(memory_values):

        for j, bit in binary_index:
            if bit == '0' and previous_bit[j] == 1:
                circuit.append(XGate(), [qaddr[j]])
            previous_bit[j] = int(bit)
        
        if normalize:
            theta = calculate_theta(el, max_value)
        else:
            theta = el 
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

    pass_manager = preset_passmanagers.generate_preset_pass_manager(
        optimization_level=opt_lvl,
        backend=GenericBackendV2(n+1)
    )

    optimized_circuit = pass_manager.run(circuit)

    return optimized_circuit, circuit
    