import re
import matplotlib.pyplot as plt
import numpy as np

def num_nodes(line):
    return re.search('Resizing cluster to (\d) nodes', line)

def parallelize_duration(line):
    return re.search('PARALLELIZE_DURATION:(\d+\.\d+)', line)

def calculation_duration(line):
    return re.search('CALCULATION_DURATION:(\d+\.\d+)', line)

def process(line):
    if num_nodes(line):
        return num_nodes(line).group(1)
    elif parallelize_duration(line):
        return parallelize_duration(line).group(1)
    elif calculation_duration(line):
        return calculation_duration(line).group(1)
    else:
        print('Unparsable log format in line:' + line)
        exit(1)

num_nodes_list = []
parallelize_duration_list = []
calculation_duration_list = []
file = 'data/svd_filtered.log'
with open(file, 'r') as f:
    current_num_node = 0
    parallellize_list = []
    calculation_list = []
    for line in f:
        if num_nodes(line):
            n = int(num_nodes(line).group(1))
            num_nodes_list.append(n)
            if n != current_num_node and n > 2:
                current_num_node = n
                parallelize_duration_list.append(np.mean(parallellize_list))
                parallellize_list = []
                calculation_duration_list.append(np.mean(calculation_list))
                calculation_list = []
        elif parallelize_duration(line):
            n = float(parallelize_duration(line).group(1))
            parallellize_list.append(n)
        elif calculation_duration(line):
            n = float(calculation_duration(line).group(1))
            calculation_list.append(n)
        else:
            print('Unparsable log format in line:' + line)
    parallelize_duration_list.append(np.mean(parallellize_list))
    calculation_duration_list.append(np.mean(calculation_list))
    
# Plot line graph with the two series parallelize and calculation (including labels)
fig,ax = plt.subplots()
ax.plot(num_nodes_list, parallelize_duration_list, 'r', label='parallelisation')
ax.plot(num_nodes_list, calculation_duration_list, 'b', label='calculation')
ax.plot(num_nodes_list, [a + b for a, b in zip(parallelize_duration_list, calculation_duration_list)], 'g', label='total')
ax.set(xlabel='Number of worker nodes', ylabel='Execution time (s)',
       title='SVD calculation')
ax.legend()
#plt.xticks(num_nodes_list)
plt.savefig("report/img/svd-speedup.pdf")
