from lib.circuit_metrics import ffqram_metrics_graycode, ffqram_metrics_classic
from matplotlib import pyplot as plt

size = range(1, 8)



optimization_levels = range(4)

for opt_level in optimization_levels:
    difference_size = []
    differnce_size_b = []

    for el in size:
        _, _, _, classic_opt = ffqram_metrics_classic(2**el, opt_lvl=opt_level)
        _, _, _, gray_opt = ffqram_metrics_graycode(2**el, opt_lvl=opt_level)
        _, _, _, classic_opt_b = ffqram_metrics_classic(2**el, opt_lvl=opt_level, barrier=False)
        _, _, _, gray_opt_b = ffqram_metrics_graycode(2**el, opt_lvl=opt_level, barrier=False)



        difference_size.append(classic_opt-gray_opt)
        differnce_size_b.append(classic_opt_b-gray_opt_b)
    plt.figure(figsize=(12, 6))

    # Tracciare Circuit Depth
    plt.subplot(1, 2, 1)
    plt.plot(size, difference_size, marker='o', color='#00A86B', linewidth=2, label='Difference of Classic and Graycode FF-QRAM Size with barrier')  # Verde
    plt.plot(size, differnce_size_b, marker='o', color='#FF7F00', linewidth=2, label='Difference of Classic and Graycode FF-QRAM Size without barrier')  # Arancione
    plt.xlabel('Address Qubit', fontsize=12)
    plt.ylabel('Difference', fontsize=12)
    plt.legend()
    plt.title(f'level of Optimization={opt_level}', fontsize=12)
        
    # Miglioramenti estetici
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()

    plt.show()