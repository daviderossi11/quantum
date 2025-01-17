from lib.circuit_metrics import ffqram_metrics_graycode, ffqram_metrics_classic
from matplotlib import pyplot as plt

size = range(1,8)
datasize = [2**i for i in size]

classic_opt_size = []
gray_opt_size = []


classic_opt_size_b = []
gray_opt_size_b = []

for el in size:
    _, _, _, classic_opt = ffqram_metrics_classic(2**el)
    _, _, _, gray_opt = ffqram_metrics_graycode(2**el)

    _, _, _, classic_opt_b = ffqram_metrics_classic(2**el, opt_lvl=0)
    _, _, _, gray_opt_b = ffqram_metrics_graycode(2**el, opt_lvl=0)
    
    classic_opt_size.append(classic_opt)
    gray_opt_size.append(gray_opt)
    classic_opt_size_b.append(classic_opt_b)
    gray_opt_size_b.append(gray_opt_b)

