import re
from tabulate import tabulate
import os

#updates 
# march 26th: 
# bonding analysis table with bond order are now printed.
#further modification is needed in order to integrate with Matt's notebook.
# 1. printed information should be displayed in the notebook
# 2. path should be read from the json file in the folder

def extract_keibo_section(file_path):
    with open(file_path, 'r')as file:
        lines = file.readlines()
                 
    start_index = -1
    end_index = -1
#extract KEI-BO section that's needed for the analysis
    for i in range(len(lines)):
        if "BOND ORDER     KEI-BO     ORB I     OCC I     ATM I     ORBTYP I     ORB J     OCC J     ATM J     ORBTYP J" in lines[i]:
            start_index = i
            print("file formatted - file name:", file_path)
        if "PRINT OFF ORIENTATION INFORMATION BY OCCUPATION MAGNITUDE." in lines[i]:
            end_index = i-2

    if start_index != -1 and end_index != -1:
        new_lines = lines[start_index:end_index-1]
        with open(file_path+".kbo",'w') as file:
            file.writelines(new_lines)
    else:
        print("file fail to be formatted - file name:", file_path)
        print("start and/or end string not found in the file")

#process the log files in the specified directory
log_directory = "/Users/shikim/pynta-quao/quao-postprocessing"
file_list = [os.path.join(log_directory,f) for f in os.listdir(log_directory) if os.path.isfile(os.path.join(log_directory, f)) and f.endswith('.log')]
#processs each file in the list
for file_path in file_list:
    extract_keibo_section(file_path)

def format_keibo_section(file_path):
    with open(file_path, 'r')as file:
        text = file.read()
                 
    pattern = r'\((.*?)\)'
# perform task 1: replace 'NO LABEL ASSIGNED YET' with 'NO_LABEL_YET'
    text = text.replace("NO LABEL ASSIGNED YET", "NO_LABEL_YET")
# perform task 2: delete spaces between words in parentheses
    text = re.sub(r'\(.*?\)', lambda x: ''.join(x.group(0).split()), text)

# perform task 3: delete spaces between 'NWB' and '0'
    text = text.replace('NWB   0', 'NWB0')

# perform task 4: delete spaces between alphabet, number, and (
    text = re.sub(r'(\w+)\s+(\d+)\s+\(', r'\1\2(', text)

# write the output file
    with open(file_path, "w") as f:
        f.write(text)
#after writing the first intermediate:
    matches = re.findall(pattern,text)

#loop through the matches and replace them with an empty string
    for match in matches:
        text = text.replace(f'({match})', '')

# write the second output file
    with open(file_path +'-atoms', "w") as f:
        f.write(text)

#process the log files in the specified directory
log_directory = "/Users/shikim/pynta-quao/quao-postprocessing"
file_list = [os.path.join(log_directory,f) for f in os.listdir(log_directory) if os.path.isfile(os.path.join(log_directory, f)) and f.endswith('.kbo')]

#processs each file in the list
for file_path in file_list:
    format_keibo_section(file_path)

def generate_keibo_tables(file_path):
    with open(file_path,'r') as file:
        rows = [line.strip().split() for line in file.readlines()[1:]]

#create entire table
    for row in rows:
        first_value = round(abs(float(row[0])),2)
        abs_first_value = abs(first_value)
        row.insert(0,first_value)

    row_sorted = sorted(rows, key=lambda x: x[0],reverse=True)
#
    headers = ['ABS BOND ORDER','BOND ORDER','KEI-BO','ORB I','OCC I','ATM I','ORBTYP I','ORB J','OCC J','ATM J','ORBTYP J']
    table = tabulate(row_sorted, headers=headers, tablefmt='outline')
#
    with open(file_path+'-atoms',"r") as file:
        rows = [line.strip().split() for line in file.readlines()[1:]]
    
    for row in rows:
        first_value = round(abs(float(row[0])),2)
        abs_first_value = abs(first_value)
        row.insert(0,first_value)

    row_sorted = sorted(rows, key=lambda x: x[0],reverse=True)
#
    headers = ['ABS BOND ORDER','BOND ORDER','KEI-BO','ORB I','OCC I','ATM I','ORBTYP I','ORB J','OCC J','ATM J','ORBTYP J']
    table = tabulate(row_sorted, headers=headers)
#
    with open(file_path+'-atoms',"w") as file:
        file.write(table)
#==
    with open(file_path+'-atoms','r') as file:
        rows = [line.strip().split() for line in file.readlines()[2:]]

    new_rows = []
    for row in rows:
        abs_kei_bo = row[0]
        atm_i = row[5]
        atm_j = row[9]
        new_row = [abs_kei_bo, atm_i, atm_j]
        new_rows.append(new_row)
    #print(new_rows)

    new_headers = ['ABS BOND ORDER', 'ATM I', 'ATM J']
    new_table = tabulate(new_rows, headers=new_headers)

    #print(new_table)
#== convert item 2 and item 3 of each list into a tuple pair
    for lst in new_rows:
        lst[1:3] = [tuple(lst[1:3])]

#create a dictionary to hold the highest item 1 value of each pair
    dict_pairs = {}
    for lst in new_rows:
        pair = lst[1]
        item1 = float(lst[0])
        if pair in dict_pairs:
            if item1 > dict_pairs[pair]:
                dict_pairs[pair] = item1
        else:
            dict_pairs[pair] = item1

    new_list = []
    for lst in new_rows:
        pair = lst[1]
        item1 = float(lst[0])
        if float(lst[0]) == dict_pairs[pair] and float(lst[0])>0.19:
            new_list.append(lst)       
        
    new_headers = ['ABS BOND ORDER', '(ATM I, ATM J)']
    new_table = tabulate(new_list, headers=new_headers)
    print(file_path+"-atoms")
    print(new_table)

#visualization of bond order on the grid
    nodes = list(set([item for sublist in new_list for item in sublist[1]]))
    nodes.sort()

#create an empty grid
    size = len(nodes)
    grid = [['... 'for x in range(size)] for y in range(size)]

#assign values to the grid from the data list
    for value, pair in new_list:
        i=nodes.index(pair[0])
        j=nodes.index(pair[1])
        grid[i][j] = value
#
#print the grid
    print('*** Absolute bond orders (Absolute bond orders >= 0.2) betwen unique atoms ***')
    print('    ', end='')
    for node in nodes:
        print(node, end='  ')
    print()
    print('   +' + '-'*(5*size) + '+')
    for i in range(size):
        print(nodes[i] + '|', end=' ')
        for j in range(size):
            print(str(grid[i][j]), end=' ')
        print('|')
    print('   +' + '-'*(5*size)+ '+')

    #specify the directory path where the log files are
log_directory = "/Users/shikim/pynta-quao/quao-postprocessing/"

#process the log files in the specified directory
file_list = [os.path.join(log_directory,f) for f in os.listdir(log_directory) if os.path.isfile(os.path.join(log_directory, f)) and f.endswith('.kbo')]

#processs each file in the list
for file_path in file_list:
    generate_keibo_tables(file_path)

    os.remove(file_path)