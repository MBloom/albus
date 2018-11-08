from __future__ import print_function, unicode_literals

import glob
import json
import os
from pprint import pprint

from PyInquirer import prompt

data_dir = 'data'
data = []


def init_data():
    global data
    for filename in glob.glob(os.path.join(data_dir, '*.json')):
        with open(filename, mode='r') as f:
            data.append(json.load(f))


def main():
    init_data()
    questions = [
        {
            'type': 'rawlist',
            'name': 'beverage',
            'message': 'Please select from a topic below',
            'choices': [obj['name'] for obj in data],
            'default': 0,
        },
    ]

    answers = prompt(questions)
    pprint(answers)
