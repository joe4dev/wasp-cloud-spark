import re

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
file = 'data/multiply_filtered.log'
with open(file, 'r') as f:
    for line in f:
        if num_nodes(line):
            n = int(num_nodes(line).group(1))
            num_nodes_list.append(n)
        elif parallelize_duration(line):
            n = float(parallelize_duration(line).group(1))
            parallelize_duration_list.append(n)
        elif calculation_duration(line):
            n = float(calculation_duration(line).group(1))
            calculation_duration_list.append(n)
        else:
            print('Unparsable log format in line:' + line)

print num_nodes_list
print parallelize_duration_list
print calculation_duration_list
