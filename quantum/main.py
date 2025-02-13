from lib.circuit_metrics import create_ffqram_gc_circuit
import numpy as np
from qiskit.quantum_info import Operator

def main():
    n = 3  # You can change this value as needed
    array_size = 2 ** n
    random_array = np.random.rand(array_size)


    circuit = create_ffqram_gc_circuit(n, memory_values=random_array, opt_lvl=2)

    print(Operator(circuit))





if __name__ == "__main__":
    main()
