import json
import csv
from lib.circuit_metrics import ffqram_metrics_classic, ffqram_metrics_graycode

# Configurazione dei parametri di test
ADDRESS_QUBITS_RANGE = list(range(1, 10))  # Da 1 a 9 qubits
OPT_LEVELS = list(range(0, 4))  # Livelli di ottimizzazione da 0 a 3
BARRIER_OPTIONS = {"no_barriers": False, "with_barriers": True}

# Funzione per raccogliere i dati delle metriche
def collect_metrics():
    data = {}
    csv_data = []

    for opt_level in OPT_LEVELS:
        data[opt_level] = {}

        for barrier_label, barrier_val in BARRIER_OPTIONS.items():
            data[opt_level][barrier_label] = {"address_qubits": ADDRESS_QUBITS_RANGE, "classic": {}, "graycode": {}}

            for n in ADDRESS_QUBITS_RANGE:
                print(f"Processing: Opt Level {opt_level}, Barrier: {barrier_label}, Qubits: {n}...")

                # Ottenere metriche per Classic e Gray Code
                metrics_classic = ffqram_metrics_classic(n, barrier=barrier_val, opt_lvl=opt_level)
                metrics_gray = ffqram_metrics_graycode(n, barrier=barrier_val, opt_lvl=opt_level)

                # Definizione delle chiavi da salvare
                metric_keys = ["original_depth", "optimized_depth", "original_size", "optimized_size", "original_ops", "optimized_ops"]
                
                # Organizza i dati in JSON
                for i, key in enumerate(metric_keys):
                    data[opt_level][barrier_label]["classic"].setdefault(key, []).append(metrics_classic[i])
                    data[opt_level][barrier_label]["graycode"].setdefault(key, []).append(metrics_gray[i])

                # Organizza i dati per il CSV
                csv_data.append([
                    opt_level, barrier_label, n, 
                    metrics_classic[0], metrics_classic[1], metrics_classic[2], metrics_classic[3],
                    metrics_gray[0], metrics_gray[1], metrics_gray[2], metrics_gray[3]
                ])

    return data, csv_data

# Funzione per salvare i dati in JSON
def save_json(data, filename="circuit_metrics_data.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"✅ JSON salvato in {filename}")

# Funzione per salvare i dati in CSV
def save_csv(csv_data, filename="circuit_metrics_data.csv"):
    headers = [
        "Opt Level", "Barrier", "Address Qubits",
        "Classic Original Depth", "Classic Optimized Depth",
        "Classic Original Size", "Classic Optimized Size",
        "Gray Code Original Depth", "Gray Code Optimized Depth",
        "Gray Code Original Size", "Gray Code Optimized Size"
    ]

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(csv_data)
    
    print(f"✅ CSV salvato in {filename}")

# Esecuzione del codice
if __name__ == "__main__":
    metrics_data, csv_data = collect_metrics()
    save_json(metrics_data)
    save_csv(csv_data)
    print("🎉 Raccolta dati completata!")
