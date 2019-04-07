import os
from collections import defaultdict
import tarfile


path = r'C:\Users\Stas\Downloads\1'

def return_all(path):
    dict1 = defaultdict(list) 
    for root, dirs, files in os.walk(path):
        for name in files:
            data_name = name.split()[0]
            dict1[data_name].append(os.path.join(path, name))
            
    for keys, values in dict1.items():
        name_data = str(keys)+ "tar.gz"
        for value in values:
            tar = tarfile.open(os.path.join(root, name_data), "w:gz")
            tar.add(value)

    tar.close()
                       
return_all(path)
