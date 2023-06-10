import os 
import json

def generate_map(path):
    dmap = {}
    with open(path) as f:
        n_lines = int(f.readline().strip())
        for i in range(n_lines):
            photo = f.readline().strip().split(' ')
            dmap[i] = {'style': photo[0], 'tags': photo[2:]}
    with open(os.path.join(os.path.dirname(map_path), os.path.split(os.path.splitext(path)[0])[1] +'.json'), 'w') as outfile:
        json.dump(dmap, outfile)

datasets_path = './datasets'
map_path = './datasets_map'

for dataset_path in os.listdir(datasets_path):
    generate_map(os.path.join(datasets_path, dataset_path))