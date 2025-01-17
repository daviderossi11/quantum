from lib.circuit_metrics import ffqram_metrics_graycode, ffqram_metrics_classic
"""
This script generates and plots the size of quantum circuits using different optimization levels and configurations.
It compares the circuit sizes for FF-QRAM with XGate and GrayCode implementations, both with and without barriers.
Functions:
- ffqram_metrics_graycode: Computes metrics for FF-QRAM using GrayCode.
- ffqram_metrics_classic: Computes metrics for FF-QRAM using XGate.
Variables:
- size: Range of sizes for the quantum circuits.
- datasize: List of data sizes corresponding to the circuit sizes.
- optimization_levels: Range of optimization levels to be tested.
The script iterates over different optimization levels and circuit sizes, computes the circuit sizes for each configuration,
and plots the results using matplotlib.
"""
from matplotlib import pyplot as plt

size = range(1, 8)
datasize = [2**i for i in size]



optimization_levels = range(4)

for opt_level in optimization_levels:
    classic_opt_size = []
    gray_opt_size = []
    classic_opt_size_b = []
    gray_opt_size_b = []

    for el in size:
        _, _, _, classic_opt = ffqram_metrics_classic(2**el, opt_lvl=opt_level)
        _, _, _, gray_opt = ffqram_metrics_graycode(2**el, opt_lvl=opt_level)
        _, _, _, classic_opt_b = ffqram_metrics_classic(2**el, opt_lvl=opt_level, barrier=False)
        _, _, _, gray_opt_b = ffqram_metrics_graycode(2**el, opt_lvl=opt_level, barrier=False)



        classic_opt_size.append(classic_opt)
        gray_opt_size.append(gray_opt)
        classic_opt_size_b.append(classic_opt_b)
        gray_opt_size_b.append(gray_opt_b)

    plt.figure(figsize=(12, 6))

    # Tracciare Circuit Depth
    plt.subplot(1, 2, 1)
    plt.plot(datasize, classic_opt_size, marker='o', color='#00A86B', linewidth=2, label='FF-QRAM Size XGate')  # Verde
    plt.plot(datasize, gray_opt_size, marker='o', color='#FF7F00', linewidth=2, label='FF-QRAM Size GrayCode')  # Arancione    
    plt.plot(datasize, classic_opt_size_b, marker='o', color='#00A86B', linewidth=2, linestyle='--', label='FF-QRAM Size XGate without barrier')  # Verde
    plt.plot(datasize, gray_opt_size_b, marker='o', color='#FF7F00', linewidth=2, linestyle='--', label='FF-QRAM Size GrayCode without barrier')
    plt.xlabel('Data Size', fontsize=12)
    plt.ylabel('Size of the Circuit', fontsize=12)
    plt.legend()
    plt.title(f'level of Optimization={opt_level}', fontsize=12)
        
    # Miglioramenti estetici
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xscale('log', base=2)
    plt.tight_layout()

    plt.show()