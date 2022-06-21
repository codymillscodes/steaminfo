import csv
import json

def csv_to_json(infile, outfile):
    cpu_dict = {}
    with open(infile, newline='') as csvfile:
        dump = csv.DictReader(csvfile)
        loop = 0
        for row in dump:
            id = row['Model']
            cpu_dict[id] = row

    print(cpu_dict)
    with open(outfile, 'w') as f:
        f.write(json.dumps(cpu_dict, indent=4))



def scan(bench, self_hw):
    if bench == 'gpu':
        with open('bench/gpu_bench.json', 'r') as f:
            gpu_dict = json.loads(bench)
        
        if self_hw in gpu_dict:
            self_rank = gpu_dict[self_hw]['Rank']

    print(self_rank)

gpu = 'RX 580 4GB'

scan('gpu', gpu)