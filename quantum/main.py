import numpy as np
import csv
import os
from qiskit.quantum_info import Statevector, state_fidelity
from lib.circuit_metrics import create_ffqram_gc_circuit, create_ffqram_circuit

def run_ffqram_multiple_seeds_to_csv():
    output_filename = "data/ffqram_fidelity_sv.csv"
    file_exists = os.path.isfile(output_filename)
    is_empty = not file_exists or os.path.getsize(output_filename) == 0

    with open(output_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Scrivi l'header solo se il file è nuovo o vuoto
        if is_empty:
            writer.writerow([
                "run_id",
                "seed",
                "qubit_address",
                "fidelity_gray_vs_classic",
                "optimization_level"
            ])



        for run_offset in range(30,40):  # 10 nuovi run
            run_id = 1 + run_offset
            seed = run_id -1
            print(f"\n===== RUN {run_id} (seed = {seed}) =====")
            np.random.seed(seed)

            for optlvl in range(4):  # Ottimizzazione 0–3
                print(f"Optimization level: {optlvl}")

                for el in range(2, 11):  # Qubit 2–10
                    print(f"\n--- Qubit address: {el} ---")

                    random_array = np.random.rand(2 ** el)
                    normalized_array = random_array / np.linalg.norm(random_array)

                    circuit_gray, _ = create_ffqram_gc_circuit(el, random_array, optlvl, True)
                    sv_gray = Statevector.from_instruction(circuit_gray)

                    circuit_classic, _ = create_ffqram_circuit(el, random_array, optlvl, True)
                    sv_classic = Statevector.from_instruction(circuit_classic)

                    fidelity = state_fidelity(sv_gray, sv_classic)
                    print(f"Fidelity Classic vs Graycode (statevector): {fidelity:.6f}")

                    writer.writerow([
                        run_id,
                        seed,
                        el,
                        fidelity,
                        optlvl
                    ])

    print(f"\nI nuovi risultati sono stati aggiunti a '{output_filename}'")

if __name__ == "__main__":
    run_ffqram_multiple_seeds_to_csv()
