from lib.circuit_metrics import ffqram_metrics_graycode, ffqram_metrics_classic
from matplotlib import pyplot as plt

size = range(1,7)
datasize = [2**i for i in size]

classic_opt_size = []
gray_opt_size = []

for el in size:
    _, _, _, classic_opt = ffqram_metrics_classic(2**el)
    _, _, _, gray_opt = ffqram_metrics_graycode(2**el)
    
    classic_opt_size.append(classic_opt)

    gray_opt_size.append(gray_opt)



print(classic_opt_size)
print(gray_opt_size)
# plot del grafico della depth


plt.figure(figsize=(12, 6))

# Tracciare Circuit Depth
plt.subplot(1, 2, 1)
plt.plot(size, classic_opt_size, marker='o', color='yellow', linewidth=2, label='FF-QRAM Depth XGate')
plt.plot(size, gray_opt_size, marker='o', color='red', linewidth=2, label='FF-QRAM Depth GrayCode')
plt.xlabel('Address Qubits')
plt.ylabel('Circuit size')
plt.legend()
plt.title('opt_lvl=2') 