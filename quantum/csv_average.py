import json
import pandas as pd

# Nome del file JSON di input
input_json_file = "metrics_results.json"

# Nome dei file di output
output_csv_file = "metrics_summary.csv"
output_json_file = "metrics_summary.json"

# Carica il file JSON
with open(input_json_file, "r") as f:
    data = json.load(f)

# Creiamo una struttura dati per raccogliere i valori medi
metrics = {}

# Iteriamo sui risultati e raccogliamo le metriche
for entry in data:
    n = entry["n"]
    opt_lvl = entry["optimization_level"]
    
    # Estraggo le metriche
    classic_depth = entry["classic"]["optimized_depth"]
    classic_size = entry["classic"]["optimized_size"]
    gray_depth = entry["graycode"]["optimized_depth"]
    gray_size = entry["graycode"]["optimized_size"]
    
    key = (n, opt_lvl)
    
    if key not in metrics:
        metrics[key] = {
            "classic_depth": [],
            "classic_size": [],
            "gray_depth": [],
            "gray_size": [],
        }
    
    metrics[key]["classic_depth"].append(classic_depth)
    metrics[key]["classic_size"].append(classic_size)
    metrics[key]["gray_depth"].append(gray_depth)
    metrics[key]["gray_size"].append(gray_size)

# Calcoliamo la media per ogni combinazione di n e opt_lvl
final_metrics = []
json_structure = {}

for (n, opt_lvl), values in sorted(metrics.items()):
    avg_classic_depth = sum(values["classic_depth"]) / len(values["classic_depth"])
    avg_classic_size = sum(values["classic_size"]) / len(values["classic_size"])
    avg_gray_depth = sum(values["gray_depth"]) / len(values["gray_depth"])
    avg_gray_size = sum(values["gray_size"]) / len(values["gray_size"])
    
    # Formattazione per il CSV
    final_metrics.append([n, opt_lvl, avg_classic_depth, avg_classic_size, avg_gray_depth, avg_gray_size])

    # Formattazione per il JSON
    if opt_lvl not in json_structure:
        json_structure[opt_lvl] = {}
    
    json_structure[opt_lvl][n] = {
        "avg_classic_depth": avg_classic_depth,
        "avg_classic_size": avg_classic_size,
        "avg_gray_depth": avg_gray_depth,
        "avg_gray_size": avg_gray_size
    }

# Creiamo il DataFrame e salviamo il CSV
df = pd.DataFrame(final_metrics, columns=["n", "optimization_level", "classic_depth", "classic_size", "gray_depth", "gray_size"])
df.to_csv(output_csv_file, index=False)

# Salviamo il file JSON
with open(output_json_file, "w") as f:
    json.dump(json_structure, f, indent=2)

print(f"File CSV salvato: {output_csv_file}")
print(f"File JSON salvato: {output_json_file}")
