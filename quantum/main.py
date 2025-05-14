import json
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# === 1. Caricamento dei dati ===
with open("data/metrics_results.json", "r") as f:
    metrics_data = json.load(f)

# === 2. Inizializzazione struttura ===
raw_data = defaultdict(lambda: defaultdict(lambda: {
    "classic_size": [],
    "gray_size": [],
    "classic_depth": [],
    "gray_depth": []
}))

# === 3. Popolamento delle liste raw ===
for entry in metrics_data:
    opt_level = entry["optimization_level"]
    n_qubits = entry["n"]
    raw_data[opt_level][n_qubits]["classic_size"].append(entry["classic"]["optimized_size"])
    raw_data[opt_level][n_qubits]["gray_size"].append(entry["graycode"]["optimized_size"])
    raw_data[opt_level][n_qubits]["classic_depth"].append(entry["classic"]["optimized_depth"])
    raw_data[opt_level][n_qubits]["gray_depth"].append(entry["graycode"]["optimized_depth"])



print("\n===== DATI RACCOLTI IN raw_data =====")
for opt_level in sorted(raw_data.keys()):
    print(f"\n--- Livello di ottimizzazione {opt_level} ---")
    for n_qubits in sorted(raw_data[opt_level].keys()):
        entry = raw_data[opt_level][n_qubits]
        print(f"\nNumero di qubit di indirizzo: {n_qubits}")
        print(f"  classic_size:  {entry['classic_size']}")
        print(f"  gray_size:     {entry['gray_size']}")
        print(f"  classic_depth: {entry['classic_depth']}")
        print(f"  gray_depth:    {entry['gray_depth']}")
