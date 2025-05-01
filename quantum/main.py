import numpy as np
import csv
from qiskit.quantum_info import Statevector, state_fidelity
from lib.circuit_metrics import create_ffqram_gc_circuit, create_ffqram_circuit

def run_ffqram_multiple_seeds_to_csv():
    output_filename = "ffqram_fidelity_sv.csv"
    optlvl = 3

    with open(output_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Header del CSV
        writer.writerow([
            "run_id",
            "seed",
            "qubit_address",
            "normalized_input_array",
            "fidelity_gray_vs_classic"
        ])

        for run_id, seed in enumerate(range(10)):  # 10 run con seed da 0 a 9
            print(f"\n===== RUN {run_id + 1} (seed = {seed}) =====")

            for el in range(2, 11):  # Qubit da 2 a 10
                print(f"\n--- Qubit address: {el} ---")

                # Imposta il seed per questa combinazione run/qubit
                np.random.seed(seed)

                # Genera array normalizzato
                random_array = np.random.rand(2 ** el)
                normalized_array = random_array / np.linalg.norm(random_array)
                print("Array normalizzato:")
                print(normalized_array)

                # FF-QRAM con Gray Code
                circuit_gray, _ = create_ffqram_gc_circuit(el, random_array, optlvl, True)
                sv_gray = Statevector.from_instruction(circuit_gray)

                # FF-QRAM classico
                circuit_classic, _ = create_ffqram_circuit(el, random_array, optlvl, True)
                sv_classic = Statevector.from_instruction(circuit_classic)

                # Calcola fidelity tra statevector
                fidelity = state_fidelity(sv_gray, sv_classic)
                print(f"Fidelity Classic vs Graycode (statevector): {fidelity:.6f}")

                # Scrive nel CSV
                writer.writerow([
                    run_id + 1,
                    seed,
                    el,
                    list(normalized_array),
                    fidelity
                ])

    print(f"\nTutti i risultati sono stati salvati in '{output_filename}'")

if __name__ == "__main__":
    run_ffqram_multiple_seeds_to_csv()
