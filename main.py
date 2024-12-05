from lib.circuit_metrics import ffqram_metrics_graycode, ffqram_metrics_classic
from matplotlib import pyplot as plt

size = range(1,8)

classic_opt_depth = []
gray_opt_depth = []

for el in size:
    _, classic_opt, _, _ = ffqram_metrics_classic(2**el)
    _, gray_opt, _, _ = ffqram_metrics_graycode(2**el)
    
    classic_opt_depth.append(classic_opt)

    gray_opt_depth.append(gray_opt)


# plot del grafico della depth


plt.figure(figsize=(12, 6))

# Tracciare Circuit Depth
plt.subplot(1, 2, 1)
plt.plot(size, classic_opt_depth, marker='o', color='yellow', linewidth=2, label='FF-QRAM Depth XGate')
plt.plot(size, gray_opt_depth, marker='o', color='red', linewidth=2, label='FF-QRAM Depth GrayCode')
plt.xlabel('Address Qubits')
plt.ylabel('Circuit Depth')
plt.legend()
plt.title('opt_lvl=2') 