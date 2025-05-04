from lib.circuit_metrics import create_ffqram_gc_circuit
from qiskit import QuantumCircuit
from qiskit.circuit.library import Initialize
from qiskit.transpiler import preset_passmanagers
from qiskit.providers.fake_provider import GenericBackendV2
import numpy as np
import csv
import os


def run_comparation(run_id, seed):
    
    with open("data/state_preparation_metrics.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
            # Write header only if the file is new or empty
        file_exists = os.path.isfile("data/state_preparation_metrics.csv")
        is_empty = not file_exists or os.path.getsize("data/state_preparation_metrics.csv") == 0
        if is_empty:
            writer.writerow([
                "N_address_qubits",
                "seed",
                "optimized_circuit_size",
                "optimized_circuit_depth",
                "optimized_circuit_gates",
                "initialize_gate_size",
                "initialize_gate_depth",
                "initialize_gate_gates"
            ])
        # Write the data
        for n in range(2, 11):
            np.random.seed(seed)  # Set seed for reproducibility
            random_array = np.random.rand(2 ** n)
            random_array = random_array / np.linalg.norm(random_array)

            # Create the circuit
            circuit_standard_ffqram, _ = create_ffqram_gc_circuit(
                n, random_array, 3, True)
            
            init_gate = Initialize(random_array)

            init_circuit = QuantumCircuit(n)
            init_circuit.append(init_gate, range(n))

            backend = GenericBackendV2(n)

            pass_manager = preset_passmanagers.get_pass_manager(
                optimization_level=3,
                layout_method="trivial",
                backend=backend
                )

            init_circuit = pass_manager.run(init_circuit)

            writer.writerow([
                n,
                seed,
                circuit_standard_ffqram.size(),
                circuit_standard_ffqram.depth(),
                circuit_standard_ffqram.count_ops(),
                init_circuit.size(),
                init_circuit.depth(),
                init_circuit.count_ops()
            ])
    print(f"\nI nuovi risultati sono stati aggiunti a 'data/state_preparation_metrics.csv'")

if __name__ == "__main__":
    for run_offset in range(1, 1):  # 10 nuovi run
        run_id = 1 + run_offset
        seed = run_id - 1
        print(f"\n===== RUN {run_id} (seed = {seed}) =====")
        run_comparation(run_id, seed)



