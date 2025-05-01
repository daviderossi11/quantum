from qiskit_aer import AerSimulator
from qiskit_ibm_runtime.fake_provider import *
from qiskit_aer.noise import NoiseModel
from qiskit.circuit.library import *
from qiskit.quantum_info import Statevector, state_fidelity, DensityMatrix
from qiskit import *
from lib.circuit_metrics import create_ffqram_gc_circuit, create_ffqram_circuit
import numpy as np
from qiskit.providers.fake_provider import *

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








n = 2  # Number of qubits
# Noisy backend instance
noisy_instance = Fake20QV1()

np.random.seed(0)  # Set seed for reproducibility


# -----------------------------

random_array = np.random.rand(2 ** n)

_, circuit_standard_ffqram = create_ffqram_circuit(
    n, random_array,0, True, False)

statevector_standard_ffqram = Statevector.from_instruction(
    circuit_standard_ffqram)  # No noise
dm_standard = DensityMatrix(statevector_standard_ffqram)

# -----------------------------

# Running the standard flip-flop qram circuit with noise
density_matrix_standard_ffqram, transpiled_circuit_standard_ffqram = run_backend(
    circuit_standard_ffqram.copy(), noisy_instance, 'density_matrix', 3)

fidelity_standard_ff_qram = state_fidelity(
   density_matrix_standard_ffqram, statevector_standard_ffqram)

print("Fidelity of standard ff-qram:", fidelity_standard_ff_qram)

# -----------------------------

_, circuit_optimized_ffqram = create_ffqram_gc_circuit(
    n, random_array,0, True, False)

# Running the optimized flip-flop qram circuit with noise
density_matrix_optimized_ff_qram, transpiled_circuit_optimized_ff_qram = run_backend(
    circuit_optimized_ffqram.copy(), noisy_instance, 'density_matrix', 3)

fidelity_standard_ff_qram_and_optimized_ff_qram = state_fidelity(
    density_matrix_optimized_ff_qram, statevector_standard_ffqram)

print("Fidelity of optimized ff-qram:",
      fidelity_standard_ff_qram_and_optimized_ff_qram)
