"""
Questo script confronta le dimensioni ottimizzate dei circuiti quantistici utilizzando due diverse codifiche: 
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
3. Traccia i grafici delle dimensioni dei circuiti per le dimensioni dei dati corrispondenti.
4. Visualizza i grafici con le etichette e i titoli appropriati.
"""
