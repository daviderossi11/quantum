from lib.circuit_metrics import ffqram_metrics_graycode, ffqram_metrics_classic

size = range(1,8)

classic_depth = []
classic_opt_depth = []

gray_depth = []
gray_opt_depth = []

for el in size:
    classic, classic_opt, _, _ = ffqram_metrics_classic(el)
    gray, gray_opt, _, _ = ffqram_metrics_graycode(el)
    
    classic_depth.append(classic)
    classic_opt_depth.append(classic_opt)
    
    gray_depth.append(gray)
    gray_opt_depth.append(gray_opt)


