"""
Script to draw tree diagrams.

Will only work for things that have 9 or less levels
"""
import re
from collections import defaultdict

f = open("group.py", "r")

tree = []
tree_dict = {}
level_dict = {}
level_list = []
labels = {}

for line in f:
    line = line.strip()
    tree.append(line)

tree = [x for x in tree if re.search(r'L\d:', x)]  # get only the strings from the tree

# getting just the labels and their indexes
for node in tree:
    split_node = re.split(' ', node)
    tree_dict[tree.index(node)] = split_node[-1]
    level_dict[tree.index(node)] = split_node[0]
    level_list.append(split_node[0])

    if split_node[-1] not in list(labels.keys()):
        labels[split_node[-1]] = 's' + str(len(labels) + 1)

levels = set()
level_list[:] = [item for item in level_list if item not in levels and not levels.add(item)]  # get the individual levels

colored = ['Ct-CtN3s',  # ndoes that should be differnt colored
'Ct-N3tN3s',
'Ct-N3tOs',
'Ct-N3tC',
'Ct-N3tCs',
'Ct-N3tCd',
'Cdd-N3dOd',
'Cdd-N3dN3d',
'Cdd-N5dc',
'Cdd-N5dcN5dc',
'Cdd-N5dcO2d',
'Cdd-N5dcCd',
'Cds-OdN1sc',
'Cds-OdN3dH',
'Cd-N3dO2s',
'Cd-N3dN3s',
'Cds-CNH',
'Cs-N3dHHH',
'Cs-N3dCHH',
'O0sc-N5dc',
'O2d-N3d',
'O2d-N5dc',
'O2s-N',
'O2s-CN',
'O2s-CsN3d',
'O2s-ON',
'O2s-OsN3d',
'O2s-NN',
'O2s-N3sN3d',
'N',
'N1dc',
'N1sc',
'N3s',
'N3s-CHH',
'N3s-Cs(OH)HH',
'N3s-CCH',
'N3s-N',
'N3s-N3dHH',
'N3s-NCH',
'N3d',
'N3d-CdO',
'N3d-CdOH',
'N3d-CdN3s',
'N3d-CddN3s',
'N3d-OdOs',
'N3d-OdN3s',
'N3d-CON3d',
'N3d-COO2d',
'N3d-COCd',
'N3d-OdC',
'N3t',
'N3t-CtN',
'N3t-CtO',
'N3t-CtC',
'N5dc',
'N5dc-O0sc',
'N5dc-OdN1scH',
'N5ddc']

# list_of_strings = ['digraph G {']
list_of_strings = ['digraph G {','center=1;']

for level in reversed(level_list[1:]):  # writing the node connections'
    level_int = level_list.index(level)
    indexes = [k for k, v in level_dict.items() if v == level]  # getting the indexes of each level
    for i in indexes:
        child_name = tree_dict[i]
        parent_level = level_int - 1
        potential_parents = [k for k, v in level_dict.items() if v == level_list[parent_level]]
        try:

            parent = i - min(y for y in [i - x for x in potential_parents] if y > 0)
            if parent < 0:
                raise
            parent_name = tree_dict[parent]
        except:
            if len(potential_parents) is 1:
                parent_name = tree_dict[0]
                print(parent_name)
            else:
                print(potential_parents)
                print('level: ', level, 'index: ', tree_dict[i])

        if tree_dict[i] in colored:
            list_of_strings.append(labels[parent_name] + ' -> ' + labels[child_name] + ' [color=red, penwidth=2, arrowsize=1];')
        else:
            list_of_strings.append(labels[parent_name] + ' -> ' + labels[child_name] + ' [penwidth=2, arrowsize=1];')

for label in labels:  # writing the species translations
    str_to_add = labels[label] + ' [ fontname="Helvetica", shape=box, label="' + label + '"];'
    list_of_strings.append(str_to_add)

for level in level_list:
    indexes = [k for k, v in level_dict.items() if v == level]
    for i in indexes:
        if i == 0:
            str_to_add = ' {rank = source; '
        else:
            str_to_add = ' {rank = same; '
        name = tree_dict[i]
        str_to_add = str_to_add + labels[name] + '; '
    str_to_add = str_to_add + '}'
    list_of_strings.append(str_to_add)

list_of_strings.append(' fontname = "Helvetica";')
list_of_strings.append('}')

with open("tree.dot",'w') as f:
    for x in list_of_strings:
        f.write('{}\n'.format(x))