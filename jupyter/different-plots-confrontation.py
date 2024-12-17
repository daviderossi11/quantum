from lib.circuit_metrics import ffqram_metrics_graycode, ffqram_metrics_classic
from matplotlib import pyplot as plt
"""
Questo script confronta le metriche di ottimizzazione dei circuiti quantistici utilizzando due diverse codifiche: 
FF-QRAM Size XGate e FF-QRAM Size GrayCode. Vengono utilizzati vari livelli di ottimizzazione e opzioni di barriera 
per valutare le prestazioni dei circuiti.
Importa le funzioni ffqram_metrics_graycode e ffqram_metrics_classic dal modulo lib.circuit_metrics e pyplot da matplotlib.
Variabili:
- size: range di dimensioni degli indirizzi dei qubit.
- datasize: lista delle dimensioni dei dati corrispondenti alle dimensioni degli indirizzi dei qubit.
- classic_opt_size: lista per memorizzare le dimensioni ottimizzate dei circuiti classici.
- gray_opt_size: lista per memorizzare le dimensioni ottimizzate dei circuiti GrayCode.
- optimization_levels: range dei livelli di ottimizzazione.
- barrier_options: lista delle opzioni di barriera (True o False).
Per ogni livello di ottimizzazione e opzione di barriera, il codice:
1. Inizializza le liste classic_opt_size e gray_opt_size.
2. Calcola le dimensioni ottimizzate dei circuiti classici e GrayCode per ogni dimensione degli indirizzi dei qubit.
3. Traccia i grafici delle profondità dei circuiti per le dimensioni dei dati corrispondenti.
4. Visualizza i grafici con le etichette e i titoli appropriati.
"""


size = range(1,7)
datasize = [2**i for i in size]

classic_opt_size = []
gray_opt_size = []



optimization_levels = range(3)
barrier_options = [True, False]

for opt_level in optimization_levels:
    for barrier in barrier_options:
        classic_opt_size = []
        gray_opt_size = []

        for el in size:
            _, _, _, classic_opt = ffqram_metrics_classic(2**el, opt_lvl=opt_level, barrier=barrier)
            _, _, _, gray_opt = ffqram_metrics_graycode(2**el, opt_lvl=opt_level, barrier=barrier)
            
            classic_opt_size.append(classic_opt)
            gray_opt_size.append(gray_opt)

        plt.figure(figsize=(12, 6))

        # Tracciare Circuit Depth
        plt.subplot(1, 2, 1)
        plt.plot(datasize, classic_opt_size, marker='o', color='orange', linewidth=2, label='FF-QRAM Size XGate')
        plt.plot(datasize, gray_opt_size, marker='o', color='green', linewidth=2, label='FF-QRAM Size GrayCode')
        plt.xlabel('Data Size')
        plt.ylabel('Size of the Circuit')
        plt.legend()
        plt.title(f'opt_lvl={opt_level}, barrier={barrier}')

        plt.tight_layout()
        plt.show()