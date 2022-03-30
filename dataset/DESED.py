import sys,os
sys.path.append("gpuRIR")

from mixing import generate

import glob
import argparse

import numpy as np
import librosa
import torch

# utils
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

# Due to 'PySoundFile failed. Trying audioread instead' 
import warnings
warnings.filterwarnings('ignore')

# param
parser = argparse.ArgumentParser()
parser.add_argument('--input_root', '-i', type=str, required=True)
parser.add_argument('--output_root', '-o', type=str, required=True)
parser.add_argument('--n_output', '-n', type=int, required=True)
args = parser.parse_args()

## ROOT
root = args.input_root
output_root = args.output_root
n_output = args.n_output

## PATH
target_list = [x for x in glob.glob(os.path.join(root,'**','*.wav'),recursive=True)]
print("Target Files : {}".format(len(target_list)))

## Gen List, 
# currently, np.random seed is fixed in MP

list_sources = []
for i in range(n_output):
    n_source = np.random.randint(low=1,high=5)
    list_sources.append(np.random.choice(target_list,n_source))

def process(idx):
    # gen random parameters
    #n_source = np.random.randint(low=1,high=4)
    #list_sources = np.random.choice(target_list,n_source)
    generate(output_root,list_sources[idx],idx,50,shift=256,match="4sec")

if __name__=='__main__': 
    cpu_num = cpu_count()

    os.makedirs(os.path.join(output_root),exist_ok=True)

    arr = list(range(n_output))
    with Pool(cpu_num) as p:
        r = list(tqdm(p.imap(process, arr), total=len(arr),ascii=True,desc='processing'))