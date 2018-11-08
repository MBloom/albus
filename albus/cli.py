from __future__ import print_function, unicode_literals

import glob
import json
import os
from pprint import pprint

from PyInquirer import prompt

data_dir = 'data'
data = {}

def init_data():
    global data
    for filename in glob.glob(os.path.join(data_dir, '*.json')):
        with open(filename, mode='r') as f:
            payload = json.load(f)
            data[payload['name']] = payload

def prompt_topic():
    init_data()
    questions = [
        {
            'type': 'rawlist',
            'name': 'topic',
            'message': 'Please select from a topic below',
            'choices': sorted([obj for obj in data]),
            'default': 0,
        },
    ]

    answer = prompt(questions)
    return answer['topic']

def prompt_executable(topic_name):
    topic = data[topic_name]
    executables = topic['executables']
    executable_name_to_executable = {executable['name']:executable for executable in executables}

    questions = [
        {
            'type': 'rawlist',
            'name': 'executable_name',
            'message': 'Please select an executable below',
            'choices': [executable_name for executable_name in executable_name_to_executable],
            'default': 0,
        },
    ]

    answer = prompt(questions)
    return executable_name_to_executable[answer['executable_name']]

def main():
    topic_name = prompt_topic()
    executable = prompt_executable(topic_name)
    pprint(executable)