from lib.circuit_metrics import ffqram_metrics_graycode, ffqram_metrics_classic
from matplotlib import pyplot as plt

size = range(1,12)

classic_opt_size = []
gray_opt_size = []

difference_size = []

for el in size:
    _, _, _, classic_opt, _, _ = ffqram_metrics_classic(el, barrier=False, opt_lvl=1)
    _, _, _, gray_opt, _, _ = ffqram_metrics_graycode(el, barrier=False, opt_lvl=1)


    difference_size.append(classic_opt - gray_opt)

for i in range(len(size)):
    print(f"Size: {size[i]}")
    print(f"Difference: {difference_size[i]}")
