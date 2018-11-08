from __future__ import print_function, unicode_literals

import sys
sys.path.append('..')

import glob
import json
import os
from pprint import pprint
from foo_checker.bazel_run import execute

from PyInquirer import prompt

data_dir = 'data'
ALPHA = os.getenv('ALPHA')

def init_data():
    data = {}
    for filename in glob.glob(os.path.join(data_dir, '*.json')):
        with open(filename, mode='r') as f:
            payload = json.load(f)
            data[payload['name']] = payload
    return data

def prompt_topic(data):    
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

def prompt_executable(topic):
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

def get_command_path(executable):
    if 'path' in executable and executable['path'] == 'alpha':
        return ALPHA
    return '.'

def main():
    all_data = init_data()
    topic = prompt_topic(all_data)
    executable = prompt_executable(all_data[topic])
    if 'command' in executable:
        execute(executable['command'], get_command_path(executable))
    elif 'executables' in executable:
        inner_executable = prompt_executable(executable)
        if 'command' in inner_executable:
            execute(inner_executable['command'], get_command_path(executable))