from lib.circuit_metrics import create_ffqram_gc_circuit
import numpy as np
from qiskit.quantum_info import Statevector
from qiskit.circuit.library import StatePreparation
from qiskit import QuantumCircuit

def extract_data_from_statevector(state_vector, n):
    """ Estrae i dati dallo statevector della FFQRAM con normalizzazione corretta """
    extracted_values = {}

    # Somma delle ampiezze dei qubit dati in |1⟩
    total_amplitude = sum(np.abs(amplitude) for i, amplitude in enumerate(state_vector) if format(i, f'0{n}b')[-1] == '1')

    for i, amplitude in enumerate(state_vector):
        binary_state = format(i, f'0{n}b')  # Converti l'indice in binario con n bit
        if binary_state[-1] == '1':  # Se il qubit dati è |1⟩, è un valore memorizzato
            address = binary_state[:-1]  # Rimuoviamo il qubit dati per ottenere solo l'indirizzo
            X_original = np.abs(amplitude) / total_amplitude  # Normalizziamo rispetto alla somma

            extracted_values[address] = X_original

    return extracted_values

def print_statevector_details(state_vector, n):
    """ Stampa gli stati e le relative ampiezze dal vettore di stato """
    print("\n🔹 Stati e ampiezze dello statevector FFQRAM:")
    for i, amplitude in enumerate(state_vector):
        binary_state = format(i, f'0{n}b')  # Converte l'indice in un numero binario con n bit
        prob = np.abs(amplitude)**2  # Probabilità dello stato
        if prob > 1e-6:  # Stampa solo gli stati con ampiezza significativa
            print(f"|{binary_state}⟩ : {amplitude.real:.4f} + {amplitude.imag:.4f}i (p={prob:.4f})")

def print_statevector(state_vector, title="State Vector"):
    """ Stampa un vettore di stato in formato colonna """
    print(f"\n🔹 {title}:")
    for amplitude in state_vector:
        print(f"| {amplitude.real:.4f} + {amplitude.imag:.4f}i |")  # Formato con parte reale e immaginaria

def main():
    n = 3  # Numero di qubit
    array_size = 2**n
    random_array = np.random.rand(array_size)  # Generiamo i dati originali

    print("\n🔹 Valori originali:")
    print(random_array)

    # **Creiamo il circuito FFQRAM**
    circuit, _ = create_ffqram_gc_circuit(n, memory_values=random_array, opt_lvl=2)
    state_vector_gc = Statevector.from_instruction(circuit)

    # **Stampa del vettore di stato della FFQRAM**
    print_statevector(state_vector_gc.data, "State Vector dalla FFQRAM")

    # **Creiamo il circuito con StatePreparation**
    state_prep = StatePreparation(random_array, normalize=True)  
    init_circuit = QuantumCircuit(n)
    init_circuit.append(state_prep, range(n))

    state_vector_init = Statevector.from_instruction(init_circuit)

    # **Stampa del vettore di stato generato con StatePreparation**
    print_statevector(state_vector_init.data, "State Vector da StatePreparation")

    # **Estrarre i valori dallo statevector FFQRAM**
    extracted_values_gc = extract_data_from_statevector(state_vector_gc.data, n+1)
    extracted_values_init = extract_data_from_statevector(state_vector_init.data, n)

    print("\n🔹 Valori estratti dallo statevector della FFQRAM:")
    for address, value in extracted_values_gc.items():
        print(f"Indirizzo: |{address}⟩ → Valore: {value:.4f}")

    print("\n🔹 Valori estratti dallo statevector di StatePreparation:")
    for address, value in extracted_values_init.items():
        print(f"Indirizzo: |{address}⟩ → Valore: {value:.4f}")

    print_statevector_details(state_vector_gc.data, n)
    print_statevector_details(state_vector_init.data, n)

if __name__ == "__main__":
    main()
