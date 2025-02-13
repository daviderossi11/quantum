import json
import csv

# Percorsi dei file
json_file = "circuit_metrics_data.json"
csv_output_file = "circuit_metrics_table.csv"

# **Leggi il file JSON**
with open(json_file, "r") as f:
    data = json.load(f)

# **Struttura del nuovo CSV**
headers = [
    "Opt Level", "Barrier", "Address Qubits",
    "Classic Original Depth", "Classic Optimized Depth",
    "Classic Original Size", "Classic Optimized Size",
    "Gray Code Original Depth", "Gray Code Optimized Depth",
    "Gray Code Original Size", "Gray Code Optimized Size"
]

# **Prepara i dati per la scrittura**
csv_rows = []

for opt_level, opt_data in data.items():
    for barrier_setting, barrier_data in opt_data.items():
        address_qubits = barrier_data["address_qubits"]
        
        # Itera su ogni valore di address qubits
        for i, n in enumerate(address_qubits):
            csv_rows.append([
                opt_level, barrier_setting, n,  # Ottimizzazione, tipo di barrier, numero qubits
                barrier_data["classic"]["original_depth"][i], 
                barrier_data["classic"]["optimized_depth"][i], 
                barrier_data["classic"]["original_size"][i], 
                barrier_data["classic"]["optimized_size"][i], 
                barrier_data["graycode"]["original_depth"][i], 
                barrier_data["graycode"]["optimized_depth"][i], 
                barrier_data["graycode"]["original_size"][i], 
                barrier_data["graycode"]["optimized_size"][i]
            ])

# **Scrivi il nuovo file CSV**
with open(csv_output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=";")  # Usa il punto e virgola per Excel
    writer.writerow(headers)  # Scrivi l'intestazione
    writer.writerows(csv_rows)  # Scrivi i dati
    
print(f"✅ CSV tabellare salvato in {csv_output_file}")
