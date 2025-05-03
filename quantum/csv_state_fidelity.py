from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel
from qiskit.circuit.library import *
from qiskit.quantum_info import Statevector, state_fidelity, DensityMatrix
from qiskit import *
from lib.circuit_metrics import create_ffqram_gc_circuit, create_ffqram_circuit
import numpy as np
from qiskit.providers.fake_provider import *
import csv

def run_backend(circuit, model_instance, method='density_matrix', optimization_level=0):
    """
    Run a quantum circuit on a backend.

    Args:
        circuit (QuantumCircuit): The quantum circuit to run.
        model_instance (BaseBackend): The backend instance.
        method (str, optional): Method for simulation. Defaults to 'density_matrix'.
        optimization_level (int, optional): Optimization level for transpiling the circuit. Defaults to 0.

    Returns:
        numpy.ndarray: Density matrix of the final state.
        QuantumCircuit: Transpiled circuit.
    """
    circuit.save_density_matrix()
    noise_model = NoiseModel.from_backend(model_instance)
    coupling_map = model_instance.configuration().coupling_map
    basis_gates = noise_model.basis_gates

    backend = AerSimulator(method=method, noise_model=noise_model,
                           coupling_map=coupling_map, basis_gates=basis_gates)

    transpiled_circuit = transpile(
        circuit, backend, optimization_level=optimization_level, coupling_map=coupling_map, layout_method="trivial")

    density_matrix = backend.run(transpiled_circuit).result().data()[
        'density_matrix']
    return density_matrix, transpiled_circuit



def run_ffqram(run_id, seed):

    filename = "data/state_fidelity_noise/ffqram_fidelity_run_id_{}.csv".format(run_id)
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Header del CSV
        writer.writerow([
            "N_address_qubits",
            "seed",
            "transpiled_classic_size",
            "transpiled_gray_size",
            "transpiled_classic_depth",
            "transpiled_gray_depth",
            "fidelity_standard",
            "fidelity_optimized",
            "optimization_level"
        ])
        np.random.seed(seed)  # Set seed for reproducibility

        for optlvl in range(4): 
            print(f"\n===== RUN {run_id} (seed = {seed}) =====")
            print(f"Optimization level: {optlvl}")

            for n in range(2, 9):
                print(f"\n--- Qubit address: {n} ---")

                # Generate a random array of size 2^n
                random_array = np.random.rand(2 ** n)

                # Noisy backend instance
                noisy_instance = Fake20QV1()
                
                # FF-QRAM con Gray Code
                circuit_gray, _= create_ffqram_gc_circuit(
                    n, random_array, 0, True, False)
                

                # FF-QRAM classico
                circuit_classic, _ = create_ffqram_circuit(
                    n, random_array, 0, True, False)
                # Calcola statevector senza rumore
                statevector_standard_ffqram = Statevector.from_instruction(
                    circuit_classic)


                # Running the standard flip-flop qram circuit with noise
                density_matrix_standard_ffqram, transpiled_circuit_standard_ffqram = run_backend(
                    circuit_classic.copy(), noisy_instance, 'density_matrix', optlvl)

                fidelity_standard = state_fidelity(
                    density_matrix_standard_ffqram, statevector_standard_ffqram)
                
    

                # Running the optimized flip-flop qram circuit with noise
                density_matrix_optimized_ff_qram, transpiled_circuit_optimized_ffqram = run_backend(
                    circuit_gray.copy(), noisy_instance, 'density_matrix', optlvl)
                
                # Calcola fidelity tra density matrix
                fidelity_optimized = state_fidelity(
                    density_matrix_optimized_ff_qram, statevector_standard_ffqram)

                print("Fidelity of optimized ff-qram:",
                      fidelity_optimized)
                
                # Scrivi i risultati nel CSV
                writer.writerow([
                    n,
                    seed,
                    transpiled_circuit_standard_ffqram.size(),
                    transpiled_circuit_optimized_ffqram.size(),
                    transpiled_circuit_standard_ffqram.depth(),
                    transpiled_circuit_optimized_ffqram.depth(),
                    fidelity_standard,
                    fidelity_optimized,
                    optlvl
                ])


if __name__ == "__main__":
    # Esegui la funzione run_ffqram con un ID di esecuzione e un seme specifici
    for i in range(21, 26):
        run_ffqram(i, i)


