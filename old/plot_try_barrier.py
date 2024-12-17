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

    _, _, _, classic_opt_b = ffqram_metrics_classic(2**el, opt_lvl=1)
    _, _, _, gray_opt_b = ffqram_metrics_graycode(2**el, opt_lvl=1)
    
    classic_opt_size.append(classic_opt)
    gray_opt_size.append(gray_opt)
    classic_opt_size_b.append(classic_opt_b)
    gray_opt_size_b.append(gray_opt_b)



# plot del grafico della size


plt.figure(figsize=(12, 6))

# Tracciare Circuit Size
plt.subplot(1, 2, 1)
plt.plot(datasize, classic_opt_size, marker='o', color='orange', linewidth=2, label='FF-QRAM Size XGate')
plt.plot(datasize, gray_opt_size, marker='o', color='red', linewidth=2, label='FF-QRAM Size GrayCode')
plt.plot(datasize, classic_opt_size_b, marker='o', color='orange', linewidth=2, linestyle='--', label='FF-QRAM Size XGate without barrier')
plt.plot(datasize, gray_opt_size_b, marker='o', color='red', linewidth=2, linestyle='--', label='FF-QRAM Size GrayCode without barrier')
plt.xlabel('Dataset size')
plt.ylabel('Circuit size')
plt.legend()
plt.title('opt_lvl=2') 


# for el in size:
#     _, _, _, classic_opt = ffqram_metrics_classic(2**el)
#     _, _, _, gray_opt = ffqram_metrics_graycode(2**el)
    
#     classic_opt_size.append(classic_opt)

#     gray_opt_size.append(gray_opt)



# print(classic_opt_size)
# print(gray_opt_size)
# # plot del grafico della depth


# plt.figure(figsize=(12, 6))

# # Tracciare Circuit Depth
# plt.subplot(1, 2, 1)
# plt.plot(size, classic_opt_size, marker='o', color='yellow', linewidth=2, label='FF-QRAM Depth XGate')
# plt.plot(size, gray_opt_size, marker='o', color='red', linewidth=2, label='FF-QRAM Depth GrayCode')
# plt.xlabel('Address Qubits')
# plt.ylabel('Circuit size')
# plt.legend()
# plt.title('opt_lvl=2') 