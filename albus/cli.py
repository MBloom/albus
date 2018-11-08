from __future__ import print_function, unicode_literals

import sys
sys.path.append('..')

import glob
import json
import os
from pprint import pprint
from foo_checker.bazel_run import execute

from fuzzywuzzy import process
from PyInquirer import prompt

data_dir = 'data'
ALPHA = os.getenv('ALPHA')

MANUAL_SEARCH = "Search manually"

def init_data():
    data = {}
    for filename in glob.glob(os.path.join(data_dir, '*.json')):
        with open(filename, mode='r') as f:
            payload = json.load(f)
            data[payload['name']] = payload
    return data

def prompt_topic(data):
    choices = sorted([obj for obj in data])
    choices.insert(0, MANUAL_SEARCH)
    #pprint([{'key': unicode(i), 'name': choices[i], 'value': choices[i]} for i in range(len(choices))])
    questions = [
        {
            'type': 'expand',
            'name': 'topic',
            'message': 'Please select from a topic below',
            'choices': [{'key': unicode(i), 'name': choices[i], 'value': choices[i]} for i in range(len(choices))],
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

# >>> choices = ["Atlanta Falcons", "New York Jets", "New York Giants", "Dallas Cowboys"]
# >>> process.extract("new york jets", choices, limit=2)
#    [('New York Jets', 100), ('New York Giants', 78)]
# >>> process.extractOne("cowboys", choices)
#    ("Dallas Cowboys", 90)
def fuzzy_search(data):
    questions = [
        {
            'type': 'input',
            'name': 'executable_name',
            'message': 'Search for an executable',
        },
    ]

    answer = prompt(questions)
    search_query = answer['executable_name']
    executables = []
    for topic in data:
        executables += data[topic]['executables']
    executables_dict = {executable['name']:executable for executable in executables}
    executable_name_match = process.extract(search_query, executables_dict.keys(), limit=1)
    return executables_dict[executable_name_match[0][0]]

def main():
    all_data = init_data()
    topic = prompt_topic(all_data)
    if topic == MANUAL_SEARCH:
        executable = fuzzy_search(all_data)
        print("Best match: {0}".format(executable['name']))
    else:
        executable = prompt_executable(all_data[topic])
    if 'command' in executable:
        execute(executable['command'], get_command_path(executable))
    elif 'executables' in executable:
        inner_executable = prompt_executable(executable)
        if 'command' in inner_executable:
            execute(inner_executable['command'], get_command_path(executable))
