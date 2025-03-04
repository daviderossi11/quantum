import random
import json
import os
from concurrent.futures import ProcessPoolExecutor
from lib.circuit_metrics import ffqram_metrics_classic, ffqram_metrics_graycode

def compute_metrics(_):
    """
    Questa funzione, ad ogni chiamata:
      - Genera un array di lunghezza 2^9 (512) con valori reali in [-100, 100].
      - Per n in [1..9], seleziona i primi 2^n valori.
      - Per ognuno dei 4 livelli di ottimizzazione (0..3), calcola i valori ottimizzati
        di size e depth per le due funzioni (classic e graycode), con barriere disabilitate.
    Ritorna una lista di dizionari, uno per ogni combinazione (n, opt_lvl).
    """

    # Genera l'array "grande" (512 reali) una volta per ogni esecuzione della funzione
    big_array = [random.uniform(-100, 100) for _ in range(512)]
    optimization_levels = [0, 1, 2, 3]

    partial_results = []

    for n in range(1, 10):
        memory_values = big_array[:2**n]

        for opt_lvl in optimization_levels:
            print(f"Processing process {os.getpid()}: n={n}, opt_lvl={opt_lvl}")
            # ffqram_metrics_classic
            (
                _,
                depth_opt_classic,
                _,
                size_opt_classic,
                _,
                _
            ) = ffqram_metrics_classic(
                n=n,
                memory_values=memory_values,
                barrier=False,
                opt_lvl=opt_lvl
            )

            # ffqram_metrics_graycode
            (
                _,
                depth_opt_gray,
                _,
                size_opt_gray,
                _,
                _
            ) = ffqram_metrics_graycode(
                n=n,
                memory_values=memory_values,
                barrier=False,
                opt_lvl=opt_lvl
            )

            # Aggiunge un record di risultato
            partial_results.append({
                "n": n,
                "optimization_level": opt_lvl,
                # Se non ti serve salvare l’array, rimuovi la riga sottostante
                "memory_values": memory_values,
                "classic": {
                    "optimized_depth": depth_opt_classic,
                    "optimized_size": size_opt_classic
                },
                "graycode": {
                    "optimized_depth": depth_opt_gray,
                    "optimized_size": size_opt_gray
                }
            })

    return partial_results


def main():
    """
    - Crea un pool di 10 processi con ProcessPoolExecutor.
    - Chiama compute_metrics() 100 volte in parallelo.
    - Raccoglie tutti i risultati in un'unica lista.
    - Se esiste già metrics_results.json, lo legge.
    - Aggiunge i nuovi risultati a quelli precedenti e salva di nuovo su metrics_results.json.
    """

    # Numero di chiamate a compute_metrics da effettuare
    num_calls = 30

    # 1) Creiamo il process pool con 10 worker
    with ProcessPoolExecutor(max_workers=10) as executor:
        # 2) Eseguiamo compute_metrics() 100 volte in parallelo
        futures = executor.map(compute_metrics, range(num_calls))

    # 3) Raccogliamo i risultati in un'unica lista
    all_results = []
    for partial_list in futures:
        all_results.extend(partial_list)

    # 4) Verifichiamo se esiste già un file JSON con risultati precedenti
    existing_results = []
    if os.path.exists("metrics_results.json"):
        try:
            with open("metrics_results.json", "r") as f:
                existing_results = json.load(f)
        except json.JSONDecodeError:
            # Se il file è vuoto o corrotto, lo ignoriamo
            existing_results = []

    # 5) Uniamo i risultati precedenti con quelli nuovi
    updated_results = existing_results + all_results

    # 6) Scriviamo il file JSON (non sovrascriviamo i vecchi dati, ma li estendiamo)
    with open("metrics_results.json", "w") as f:
        json.dump(updated_results, f, indent=2)

if __name__ == "__main__":
    main()
