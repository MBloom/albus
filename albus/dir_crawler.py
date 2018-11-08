import glob
import json
import os
from pprint import pprint



for filename in glob.glob(os.path.join(topics_dir, '*.json')):
    with open(filename, mode='r') as f:
        data = json.load(f)
    pprint(data)
